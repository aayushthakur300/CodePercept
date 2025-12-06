import os
import sqlite3
import json
import re  # 🔹 for JSON fence cleanup like in Node.js
from contextlib import asynccontextmanager # 🔹 Required for lifespan
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import traceback

# 🔹 FIX: Load .env file explicitly so os.getenv finds the key
try:
    from dotenv import load_dotenv  # pip install python-dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, we continue.
    pass

# 🔹 UPDATED IMPORT: Using Supreme Verification
from language_detector import verify_submission, friendly_name
from utils.line_numbers import add_line_numbers
from utils.json_extract import extract_json_from_text  # still used elsewhere if you want
from utils.prompt_loader import PromptLoader
import test_samples  # ensures tests/samples available
import run_tests

# --- AI client wrapper (pluggable) ---
try:
    import google.generativeai as genai  # pip install google-generative-ai
    GENAI_AVAILABLE = True
except Exception:
    genai = None
    GENAI_AVAILABLE = False

# Now that load_dotenv() is called, this should pick up the key from .env
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_ANALYZE_NAME = "gemini-2.5-flash"
MODEL_FULLFIX_NAME = "gemini-2.5-flash-lite"

def call_model(prompt: str, model_name: str = MODEL_ANALYZE_NAME):
    """
    Correct Gemini API call using GenerativeModel (current official SDK).
    Used by /assistant and others.
    """
    if not API_KEY:
        # Try fallbacks if global is empty
        if not os.getenv("GOOGLE_API_KEY"):
             raise RuntimeError("Missing GEMINI_API_KEY or GOOGLE_API_KEY")

    if not GENAI_AVAILABLE:
        raise RuntimeError("google-generativeai package not installed")

    try:
        # Use dynamic check to catch env var if set after script start
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY") or API_KEY)

        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            return response.text

        parts = []
        for cand in getattr(response, "candidates", []) or []:
            content = getattr(cand, "content", None)
            if not content:
                continue
            for part in getattr(content, "parts", []) or []:
                text = getattr(part, "text", "")
                if text:
                    parts.append(text)

        if parts:
            return "\n".join(parts)

        return str(response)

    except Exception as e:
        raise RuntimeError(f"Gemini API failed: {e}")

# --- Prompt loader ---
BASE_DIR = Path(__file__).parent
prompts_dir = BASE_DIR / "prompts"
prompt_loader = PromptLoader(prompts_dir)

# --- Database (sqlite) setup ---
DB_PATH = BASE_DIR / "app.db"
conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS ai_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    ai_response TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS code_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT,
    language TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT,
    code TEXT,
    language TEXT,
    is_favorite INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")
conn.commit()

# --------------------------------------------------------------------
# 🔹 LIFESPAN EVENT HANDLER
# --------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup Logic ---
    print("🔍 Loading prompts...")
    try:
        prompt_loader.reload()
        print("📄 Prompts loaded.")
    except Exception as e:
        print("⚠ Failed loading prompts:", e)
    
    # Print Clickable Link
    port = os.getenv("PORT", "3001")
    print(f"\n{'-'*50}")
    print(f"🚀 Server running!")
    print(f"👉 Open this link: http://localhost:{port}/")
    print(f"{'-'*50}\n")
    
    yield  # Control is yielded to the application
    
    # --- Shutdown Logic (Optional) ---
    print("🛑 Shutting down server...")

# --- FastAPI app (Initialized ONCE with lifespan) ---
app = FastAPI(lifespan=lifespan, debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from main/ and public/ like Node did
MAIN_DIR = BASE_DIR / "main"
PUBLIC_DIR = BASE_DIR / "public"

# ✅ Serve style.css and script.js from backend/main/
@app.get("/style.css")
async def serve_style():
    file = MAIN_DIR / "style.css"
    if file.exists():
        return FileResponse(str(file))
    return JSONResponse({"error": "style.css not found"}, status_code=404)

@app.get("/script.js")
async def serve_script():
    file = MAIN_DIR / "script.js"
    if file.exists():
        return FileResponse(str(file))
    return JSONResponse({"error": "script.js not found"}, status_code=404)

# 🔹 Home route serving main/index.html
@app.get("/")
async def home():
    file = MAIN_DIR / "index.html"
    if file.exists():
        return FileResponse(str(file))
    return JSONResponse(
        {"status": "error", "message": "index.html not found in main/"},
        status_code=404,
    )

# 🔹 /login route that redirects to /logicprobe (like your Node flow)
@app.get("/login")
async def login_redirect():
    return RedirectResponse(url="/logicprobe")

# --- Utility route similar to /logicprobe ---
@app.get("/logicprobe")
async def logicprobe():
    file = MAIN_DIR / "logicprobe.html"
    if file.exists():
        return FileResponse(str(file))
    return JSONResponse({"status": "error", "message": "logicprobe.html not found"}, status_code=404)

# --- Prompt reload route ---
@app.post("/reload-prompts")
async def reload_prompts():
    try:
        prompt_loader.reload()
        return {"status": "success", "message": "Prompts reloaded."}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

# --- /explain endpoint ---
class ExplainPayload(BaseModel):
    code: str
    language: str
    mode: str = None
    wantCorrected: bool = False

@app.post("/explain")
async def explain(payload: ExplainPayload):
    code = payload.code or ""
    language = payload.language or ""
    include_corrected = (payload.mode == "full_fix") or payload.wantCorrected

    # --------------------------------------------------------------------
    # 🔹 SUPREME LANGUAGE VERIFICATION (Replaces old logic)
    # --------------------------------------------------------------------
    is_valid, detected_key = verify_submission(code, language)

    # STRICT ENFORCEMENT: If language doesn't match, return specific STATUS.
    if not is_valid:
        detected_display = friendly_name.get(detected_key, "Unknown/Ambiguous")
        selected_display = friendly_name.get(language, language)
        
        # We return a specific JSON object so the frontend can display the message gracefully.
        return {
            "status": "language_mismatch",
            "detected": detected_display,
            "selected": selected_display,
            "message": f"❌ LANGUAGE MISMATCH: You selected '{selected_display}', but the detector found '{detected_display}'. Only valid {selected_display} code is accepted."
        }

    # Line numbering for prompts (same behavior as before)
    numbered_code = add_line_numbers(code)

    # --------------------------------------------------------------------
    # STEP 1 — ANALYSIS (mirror Node.js behavior for JSON handling)
    # --------------------------------------------------------------------
    analysis_prompt = prompt_loader.analysis_prompt
    analysis_prompt = analysis_prompt.replace("{{LANGUAGE}}", language).replace("{{NUMBERED_CODE}}", numbered_code)
    if include_corrected:
        analysis_prompt = analysis_prompt.replace("{{INCLUDE_CORRECTED}}", ', "corrected_code": "<PROVIDE_CODE>"')
    else:
        analysis_prompt = analysis_prompt.replace("{{INCLUDE_CORRECTED}}", "")

    try:
        # 🔹 FIX: Check environment dynamically to avoid 'No API_KEY' crash
        current_key = os.getenv("GOOGLE_API_KEY") or API_KEY
        if not current_key:
             raise ValueError("Missing API Key. Please set GEMINI_API_KEY or GOOGLE_API_KEY.")

        genai.configure(api_key=current_key)
        model_analysis = genai.GenerativeModel(MODEL_ANALYZE_NAME)
        resp = model_analysis.generate_content(analysis_prompt)

        # Node: const text = await raw.response.text();
        # Python: prefer resp.text, fallback to str(resp)
        raw_text = getattr(resp, "text", None) or ""
        if not raw_text and hasattr(resp, "response") and callable(getattr(resp.response, "text", None)):
            raw_text = resp.response.text()  # just in case SDK exposes it this way

        if not raw_text:
            raw_text = str(resp)

        # Clean like Node: text.replace(/```json|```/g, '').trim();
        cleaned = re.sub(r"```json|```", "", raw_text).strip()
        analysis_result = json.loads(cleaned)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"status": "error", "message": "AI analysis failed.", "detail": str(e)}, status_code=500)

    # Block full_fix if analysis says success
    if include_corrected and analysis_result.get("status") == "success":
        return {"status": "full_fix_not_allowed", "message": "Full Fix is only allowed when errors exist."}

    # --------------------------------------------------------------------
    # STEP 2 — FULL FIX (mirror Node.js JSON handling)
    # --------------------------------------------------------------------
    fullfix_prompt = prompt_loader.fullfix_prompt
    fullfix_prompt = fullfix_prompt.replace("{{LANGUAGE}}", language).replace("{{NUMBERED_CODE}}", numbered_code)
    if include_corrected:
        fullfix_prompt = fullfix_prompt.replace("{{INCLUDE_CORRECTED}}", ', "corrected_code": "<PROVIDE_CODE>"')
    else:
        fullfix_prompt = fullfix_prompt.replace("{{INCLUDE_CORRECTED}}", "")

    try:
        # 🔹 FIX: Apply same robust key check for full fix
        current_key = os.getenv("GOOGLE_API_KEY") or API_KEY
        if not current_key:
             raise ValueError("Missing API Key. Please set GEMINI_API_KEY or GOOGLE_API_KEY.")

        genai.configure(api_key=current_key)
        model_full = genai.GenerativeModel(MODEL_FULLFIX_NAME)
        resp_full = model_full.generate_content(fullfix_prompt)

        raw_full = getattr(resp_full, "text", None) or ""
        if not raw_full and hasattr(resp_full, "response") and callable(getattr(resp_full.response, "text", None)):
            raw_full = resp_full.response.text()

        if not raw_full:
            raw_full = str(resp_full)

        cleaned_full = re.sub(r"```json|```", "", raw_full).strip()
        json_full = json.loads(cleaned_full)

        return JSONResponse(json_full)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"status": "error", "message": "AI full fix failed.", "detail": str(e)}, status_code=500)

# --- /assistant endpoint ---
class AssistantPayload(BaseModel):
    message: str

@app.post("/assistant")
async def assistant(payload: AssistantPayload):
    message = payload.message or ""
    
    if not message.strip():
        return {"status": "error", "message": "Message is required."}
    try:
        prompt = f'You are an AI coding assistant. Answer clearly.\nUser asked:\n"{message}"'
        raw = call_model(prompt, MODEL_ANALYZE_NAME)
        ai_text = raw if isinstance(raw, str) else str(raw)

        cursor.execute("INSERT INTO ai_chat (user_message, ai_response) VALUES (?, ?)", (message, ai_text))
        conn.commit()
        return {"status": "success", "reply": ai_text}
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"status": "error", "message": "AI assistant failed.", "detail": str(e)}, status_code=500)

# --- SQLite routes (same names as Node) ---
class SaveCodePayload(BaseModel):
    code: str
    language: str

@app.post("/save-code")
async def save_code(payload: SaveCodePayload):
    try:
        cursor.execute("INSERT INTO code_history (code, language) VALUES (?, ?)", (payload.code, payload.language))
        conn.commit()
        return {"status": "success", "id": cursor.lastrowid}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

@app.get("/load-last-code")
async def load_last_code():
    try:
        cursor.execute("SELECT * FROM code_history ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return {"status": "success", "data": None}
        cols = [d[0] for d in cursor.description]
        return {"status": "success", "data": dict(zip(cols, row))}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

@app.get("/load-chat")
async def load_chat():
    try:
        cursor.execute("SELECT * FROM ai_chat ORDER BY id ASC")
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        return {"status": "success", "chat": [dict(zip(cols, r)) for r in rows]}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

class SaveProjectPayload(BaseModel):
    projectName: str
    code: str
    language: str

@app.post("/save-project")
async def save_project(payload: SaveProjectPayload):
    try:
        cursor.execute("INSERT INTO projects (project_name, code, language) VALUES (?, ?, ?)", (payload.projectName, payload.code, payload.language))
        conn.commit()
        return {"status": "success", "id": cursor.lastrowid}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

@app.get("/projects")
async def get_projects():
    try:
        cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        return {"status": "success", "projects": [dict(zip(cols, r)) for r in rows]}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

class FavoritePayload(BaseModel):
    id: int
    fav: bool

@app.post("/favorite-project")
async def favorite_project(payload: FavoritePayload):
    try:
        cursor.execute("UPDATE projects SET is_favorite = ? WHERE id = ?", (1 if payload.fav else 0, payload.id))
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)

class DeletePayload(BaseModel):
    id: int

@app.post("/delete-project")
async def delete_project(payload: DeletePayload):
    try:
        cursor.execute("DELETE FROM projects WHERE id = ?", (payload.id,))
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=500)