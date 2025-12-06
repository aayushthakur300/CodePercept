import re

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------

friendly_name = {
    "c": "C", "cpp": "C++", "java": "Java", "javascript": "JavaScript",
    "typescript": "TypeScript", "python": "Python", "go": "Go", "rust": "Rust",
    "r": "R", "php": "PHP", "perl": "Perl", "ruby": "Ruby", "swift": "Swift",
    "kotlin": "Kotlin", "dart": "Dart", "matlab": "MATLAB", "sql": "SQL",
    "html": "HTML", "css": "CSS", "elixir": "Elixir", "csharp": "C#",
    "unknown": "Unknown",
}

SUPPORTED_LANG_KEYS = list(friendly_name.keys())

# ------------------------------------------------------------------
# CORE LOGIC
# ------------------------------------------------------------------

def normalize_selected_language(lang: str) -> str:
    """Normalizes user input to a standard key."""
    if not lang: return "unknown"
    s = str(lang).strip().lower()
    
    if s in ("c++", "cpp"): return "cpp"
    if s in ("c#", "csharp"): return "csharp"
    if s in ("js", "javascript", "node"): return "javascript"
    if s in ("ts", "typescript"): return "typescript"
    if s.startswith("py"): return "python"
    if s.startswith("go"): return "go"
    if s.startswith("rb"): return "ruby"
    if s.startswith("php"): return "php"
    if s.startswith("matlab"): return "matlab"
    
    return re.sub(r"\s+", "", s)

def detect_language(code: str) -> str:
    """
    Supreme Detection Engine v5.9 (MATLAB/R Fix).
    - Added 'disp' and semicolon logic for MATLAB.
    - Added 'print' and semicolon logic for R to beat Python in generic scripts.
    """
    if not code or not isinstance(code, str): return "unknown"
    
    scores = {k: 0 for k in SUPPORTED_LANG_KEYS}

    # ==========================================================
    # 1. C / C++ / C# / Java (The C-Family)
    # ==========================================================
    
    # C++
    if re.search(r"#include\s+<(iostream|vector|string|algorithm|map|set|queue|stack|list|memory|fstream)>", code): scores["cpp"] += 100
    if re.search(r"\busing\s+namespace\s+std;", code): scores["cpp"] += 100
    if re.search(r"\bstd::", code) or re.search(r"\bcout\s*<<", code): scores["cpp"] += 50
    if re.search(r"\btemplate\s*<", code): scores["cpp"] += 50
    
    # C
    if re.search(r"#include\s+<stdio\.h>", code): scores["c"] += 100
    if re.search(r"\bprintf\s*\(", code): scores["c"] += 20
    if re.search(r"\bstruct\s+\w+\s*\{", code) and not scores["cpp"]: scores["c"] += 20
    
    # Java
    if re.search(r"\bpublic\s+static\s+void\s+main\s*\(String", code): scores["java"] += 100
    if re.search(r"\bSystem\.out\.print", code): scores["java"] += 80
    if re.search(r"\bimport\s+java\.", code): scores["java"] += 60

    # C#
    if re.search(r"\busing\s+System;", code): scores["csharp"] += 100
    if re.search(r"\bConsole\.Write", code): scores["csharp"] += 80
    if re.search(r"\bpublic\s+class\s+\w+", code) and re.search(r"\{\s*get;\s*set;\s*\}", code): scores["csharp"] += 50

    # ==========================================================
    # 2. Scripting (Python, Ruby, Perl, PHP)
    # ==========================================================

    # Python
    if re.search(r"\bdef\s+\w+\(.*\):", code): scores["python"] += 60
    if re.search(r"^\s*print\(", code, re.MULTILINE): scores["python"] += 20
    if re.search(r"\[.*for\s+\w+\s+in\s+.*\]", code): scores["python"] += 50
    if re.search(r"\bimport\s+[\w\.]+", code) or re.search(r"\bfrom\s+[\w\.]+\s+import", code): 
        scores["python"] += 50
    if re.search(r":\s*$", code, re.MULTILINE): scores["python"] += 20
    if re.search(r"\belif\b", code) or "if __name__" in code: scores["python"] += 50

    # Ruby
    if re.search(r"\bdef\s+\w+", code) and re.search(r"\bend\b", code): scores["ruby"] += 50
    if re.search(r"\bputs\b", code): scores["ruby"] += 40
    if re.search(r"\battr_accessor\b", code): scores["ruby"] += 50
    if re.search(r"\.times\s+do\b", code): scores["ruby"] += 30

    # PHP
    if "<?php" in code or "<?=" in code: scores["php"] += 200
    if re.search(r"\$\w+", code): scores["php"] += 30
    if re.search(r"\bfunction\s+\w+\(", code): scores["php"] += 30 

    # Perl
    if re.search(r"\bmy\s*\(?\s*\$\w+", code): scores["perl"] += 60
    if re.search(r"\buse\s+strict;", code): scores["perl"] += 60
    if re.search(r"\bsub\s+\w+\s*\{", code): scores["perl"] += 80 

    # ==========================================================
    # 3. Web (JS, TS, HTML, CSS, Dart, Elixir)
    # ==========================================================

    # JavaScript
    if re.search(r"\bconsole\.(log|warn|error|info)\(", code): scores["javascript"] += 40
    if re.search(r"\bvar\s+\w+\s*=", code): scores["javascript"] += 20
    if re.search(r"\bconst\s+\w+\s*=", code): scores["javascript"] += 20
    if re.search(r"\bfunction\s+\w+\s*\(", code): scores["javascript"] += 30
    if re.search(r"\bimport\s+.*\s+from\s+['\"]", code): scores["javascript"] += 30
    if re.search(r"\bexport\s+(default\s+)?(const|function|class|let|var)", code): scores["javascript"] += 30
    if re.search(r"\b(document|window|global|process)\.", code): scores["javascript"] += 20
    if re.search(r"\bJSON\.(parse|stringify)", code): scores["javascript"] += 20
    if "=>" in code: scores["javascript"] += 20

    # TypeScript
    if re.search(r":\s*(string|number|boolean|any|void|unknown|never|object)\b", code): scores["typescript"] += 60
    if re.search(r"\binterface\s+[A-Z]\w*", code): scores["typescript"] += 60
    if re.search(r"\btype\s+\w+\s*=", code): scores["typescript"] += 50
    if re.search(r"\benum\s+\w+", code): scores["typescript"] += 50
    if re.search(r"\bimplements\s+\w+", code): scores["typescript"] += 50
    if re.search(r"\bas\s+[A-Z]\w*", code): scores["typescript"] += 30 
    if re.search(r"\breadonly\s+", code): scores["typescript"] += 30

    # HTML
    if re.search(r"<!DOCTYPE\s+html>", code, re.IGNORECASE): scores["html"] += 200
    if re.search(r"<\/?(html|body|div|span|h1|p|script|style|ul|li|table)\b", code, re.IGNORECASE): scores["html"] += 50

    # CSS
    if re.search(r"([.#:@][\w-]+\s*|[a-z0-9]+\s*)\{[^{}]*:[^{}]*\}", code, re.IGNORECASE):
        scores["css"] += 80
    if "--" in code and re.search(r"--[\w-]+\s*:", code): 
        scores["css"] += 60
    if re.search(r"@(media|import|keyframes|font-face|charset)\b", code): 
        scores["css"] += 60
    if re.search(r":\s*#[0-9a-fA-F]{3,6}\b", code): scores["css"] += 20
    if re.search(r"\b(px|rem|em|vh|vw|rgba|hsl)\b", code): scores["css"] += 20

    # Dart
    if re.search(r"\bvoid\s+main\(\)", code): scores["dart"] += 50
    if re.search(r"Future<.*>", code): scores["dart"] += 50 
    if re.search(r"\bimport\s+['\"]package:", code): scores["dart"] += 60

    # Elixir
    if re.search(r"\bdefmodule\b", code): scores["elixir"] += 100
    if "|>" in code: scores["elixir"] += 50
    if re.search(r"\bdef\s+.*\s+do\b", code): scores["elixir"] += 80 

    # ==========================================================
    # 4. Systems / Data (Go, Rust, Swift, Kotlin, R, MATLAB, SQL)
    # ==========================================================

    # Go
    if re.search(r"^package\s+main", code, re.MULTILINE): scores["go"] += 100
    if re.search(r"\bfunc\s+\w+\(", code): scores["go"] += 30 
    if re.search(r"chan\s+\w+", code): scores["go"] += 60 
    if ":=" in code: scores["go"] += 20

    # Rust
    if re.search(r"\bfn\s+main\(", code): scores["rust"] += 80
    if re.search(r"\bimpl\s+\w+", code): scores["rust"] += 60
    if re.search(r"println!\(", code): scores["rust"] += 60
    
    # Swift
    if re.search(r"\bimport\s+(Swift|Foundation|UIKit|SwiftUI)", code): scores["swift"] += 80
    if re.search(r"\bfunc\s+\w+\(.*\)\s*->", code): scores["swift"] += 50 
    if re.search(r"\bguard\s+let\b", code): scores["swift"] += 50

    # Kotlin
    if re.search(r"\bfun\s+main\(", code): scores["kotlin"] += 80
    if re.search(r"\bdata\s+class\s+\w+", code): scores["kotlin"] += 60
    if re.search(r"\bval\s+\w+", code) and "fun" in code: scores["kotlin"] += 20

    # R (FIXED)
    # R uses <- but also =, so we must detect standard R functions and use semicolons as a tie-breaker against Python.
    if re.search(r"\w+\s*<-", code): scores["r"] += 50
    if re.search(r"\w+\s*<-\s*(data\.frame|c\(|rnorm|read\.)", code): scores["r"] += 80
    if "%>%" in code: scores["r"] += 60
    # Added: R standard print/cat functions (shared with Python but needed for generic R scripts)
    if re.search(r"\b(print|cat|paste|head|tail|summary|plot)\s*\(", code): scores["r"] += 20
    # Added: R often uses semicolons for one-liners (Python can, but it's rare). 
    # This acts as a tiebreaker for 'a=1;print(a)' style code.
    if ";" in code and not re.search(r"^\s*(import|def|class)\s+", code, re.MULTILINE): 
        scores["r"] += 15

    # MATLAB (FIXED)
    # Added 'disp', 'size', 'length' and logic to detect trailing semicolons which suppresses output
    if re.search(r"^\s*%.*", code, re.MULTILINE) and not re.search(r"#", code): scores["matlab"] += 40
    if re.search(r"=\s*\[.*?\];?", code, re.DOTALL): scores["matlab"] += 30 
    if re.search(r"\b(disp|numel|zeros|ones|eye|repmat|linspace|mod|size|length|plot|fprintf)\s*\(", code): scores["matlab"] += 50
    if re.search(r"\[.*~.*\]\s*=", code): scores["matlab"] += 60 
    # Added: MATLAB often ends lines with semicolons to suppress output
    if re.search(r";\s*$", code, re.MULTILINE): scores["matlab"] += 20
    # Added: 'end' keyword is common in MATLAB (function/if/for end)
    if re.search(r"\bend\s*$", code, re.MULTILINE) and not re.search(r"def ", code): scores["matlab"] += 20

    # SQL
    if re.search(r"^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\b", code, re.IGNORECASE | re.MULTILINE): scores["sql"] += 60

    # ==========================================================
    # 5. ARBITRATION (The Tie Breakers)
    # ==========================================================

    # Python vs MATLAB
    if scores["python"] > 0 or re.search(r"(^|\s)#", code):
        # Only allow MATLAB if explicit MATLAB comment % exists and no Python imports
        if not re.search(r"^\s*%", code, re.MULTILINE) and not scores["matlab"] > 60:
            scores["matlab"] = 0

    # Go vs R
    if "<-" in code:
        if scores["go"] > 0: scores["r"] = 0
        elif scores["r"] > 50: scores["go"] = 0
        if ":=" in code: scores["r"] = 0
    
    # Perl vs PHP
    if scores["perl"] > 0 and re.search(r"\bsub\s+\w+", code): scores["php"] = 0
    if scores["php"] > 0 and re.search(r"\bfunction\s+\w+", code): scores["perl"] = 0

    # Elixir vs Ruby
    if scores["elixir"] >= 80: scores["ruby"] = 0

    # C++ vs HTML / Dart vs HTML
    if scores["cpp"] >= 50: scores["html"] = 0
    if scores["dart"] >= 50: scores["html"] = 0
    
    # TypeScript swallows JS
    if scores["typescript"] > 0: scores["javascript"] = 0

    # JS vs CSS arbitration
    has_js_keywords = re.search(r"\b(const|let|var|function|return|import|export)\b", code)
    if has_js_keywords:
        if not re.search(r"([.#:][\w-]+\s*)\{", code): 
            scores["css"] = 0
            
    # CSS vs JS Object arbitration
    if scores["css"] > 0 and (re.search(r"=>", code) or re.search(r"\bexport\b", code)):
        scores["css"] = 0

    # Find the winner
    best = "unknown"
    best_score = 0
    for k, v in scores.items():
        if v > best_score:
            best = k
            best_score = v

    return best

def verify_submission(code: str, selected_language: str):
    """
    The Supreme Judge.
    Returns: (is_valid: bool, detected_lang: str)
    """
    selected_norm = normalize_selected_language(selected_language)
    detected_lang = detect_language(code)
    
    # 1. Exact Match
    if detected_lang == selected_norm:
        return True, detected_lang
    
    # 2. Strict Rejection
    return False, detected_lang

# --- TEST AREA ---
if __name__ == "__main__":
    # Test your failing cases here
    print("Test 1 (MATLAB):", detect_language("a=4;b=12; disp(a+b)")) 
    print("Test 2 (R):", detect_language("a=3;b=9\nprint(a+b)"))