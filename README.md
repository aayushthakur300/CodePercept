# 🚀 CodePercept — Intelligent Code Analysis & Language Detection Engine

**CodePercept** is a **high-performance code analysis** .

It identifies 20+ languages, explains code line-by-line, detects mismatches, locates errors precisely, and auto-fixes incorrect code — all via a fast, scalable REST API.

---

## ✨ Core Highlights

### 🔹 AI-Powered Capabilities
👉 **Supports 20+ Programming Languages** 👉 **Auto Language Detection & Mismatch Alerts** 👉 **Line-by-Line Code Explanation** 👉 **Exact Error Line Detection** 👉 **One-Click Full Auto Code Fix** 👉 **Instant Debugging & Correction** 👉 **Beginner-Friendly Explanations** 👉 **Real-Time Code Analysis** 👉 **And many more…**

### ⚙️ Backend Feature Set
* **🔍 Supreme Language Detection** Accurately detects languages (C, C++, Java, Python, MATLAB, R, etc.) using weighted heuristics.
* **⚖️ Conflict Arbitration** Advanced tie-breaker logic for ambiguous cases (e.g., Python vs. MATLAB) via weighted scoring.
* **⚡ REST API Architecture** FastAPI-powered backend designed for high throughput and easy integration.
* **🗄️ Database Integration** SQLite-backed storage for application data, user logs, and metadata.
* **🧩 Prompt Management** Modular utilities for loading and managing system prompts cleanly.
* **🛠️ Extensible Utilities** Scripts for JSON extraction, line numbering, and preprocessing.

---

## 🛠️ Technology Stack

* **Framework:** Python (FastAPI + Uvicorn)
* **Database:** SQLite (`app.db`)
* **Core Logic:** Regex-based heuristics + weighted scoring
* **Environment:** `.env` configuration (dotenv)

---

## 📁 Project Structure

CodePercept/
└── backend/
    ├── database/            # DB configs & migrations
    ├── main/                # Routers & core logic
    ├── prompts/             # System prompts
    ├── utils/               # Helper utilities
    ├── .env                 # Environment config
    ├── .env.example         # Sample env file
    ├── .gitignore           # Git ignore rules
    ├── app.db               # SQLite database
    ├── db.js                # DB utility (optional Node)
    ├── language_detector.py # Supreme Detection Engine
    ├── main.py              # FastAPI entry point
    ├── run_tests.py         # Test runner
    └── test_samples.py      # Regression samples

📦 Installation & Setup
Prerequisites


a. Python 3.8+

b. Node.js (Optional — only if using db.js)

1. Clone Repository
    git clone <repository-url>
    cd backend

   
3. Configure Environment
   cp .env.example .env
    # Open .env and fill in required variables (DB path, API keys, etc.)

   
3. Install Dependencies
   pip install -r requirements.txt

   
If you don’t have a requirements file yet:
    pip install fastapi uvicorn python-dotenv
    
4. Start the Server
   uvicorn main:app --reload --port 3001
The API will run at: http://localhost:3001🧪

🧪 TestingRun the built-in test suite to verify detection accuracy and isolation logic:
python run_tests.py


Includes:


a. Accuracy Testing: Confirm correct language detection.

b. Isolation Testing: Reject wrong-language submissions with strict validation.

c. Regression Coverage: Ensures new changes don't break existing logic.


📡 API Endpoints (Example)

Method,Endpoint,Description
GET,/,Health check / Status
POST,/detect,Detects language from code snippet
POST,/analyze,Performs line-by-line analysis
POST,/fix,Auto-fixes code errors


🤝 Contributing

1. Fork the repo

2. Create a new branch

3. Commit your changes

4. Run tests using python run_tests.py


📄 License

Developed for educational and development use.

Powered by CodePercept Backend
