CodePercept
CodePercept is an intelligent code analysis and language detection engine exposed via a high-performance REST API. At its core, it utilizes the "Supreme Detection Engine v5.9" to accurately identify programming languages using advanced heuristics, resolving complex ambiguities between syntactically similar languages (e.g., MATLAB vs. Python, C vs. C++).

This backend service is designed to be the robust foundation for code processing applications, offering capabilities for language detection, prompt management, and database integration.

🚀 Features
Supreme Language Detection: Instantly identifies 21+ languages (C, C++, Java, Python, MATLAB, R, etc.) with high precision.

Conflict Arbitration: sophisticated logic to handle "tie-breaker" scenarios using weighted scoring.

REST API Architecture: Built with FastAPI for high performance and easy integration.

Database Integration: SQLite integration for storing application data.

Prompt Management: dedicated utilities for loading and managing system prompts.

Extensible Utils: Modular utility scripts for JSON extraction and line numbering.

🛠️ Technology Stack
Framework: Python (FastAPI/Uvicorn)

Database: SQLite (app.db)

Core Logic: Regular Expressions & Heuristics

Environment: Dotenv for configuration

📂 Project Structure
Plaintext

CodePercept/
└── backend/
    ├── database/            # Database configurations and migrations
    ├── main/                # Application routers and core logic
    ├── prompts/             # System prompts and templates
    ├── utils/               # Helper scripts
    ├── .env                 # Environment configuration (API Keys, Secrets)
    ├── .env.example         # Example environment file
    ├── .gitignore           # Git ignore rules
    ├── app.db               # SQLite Database file
    ├── db.js                # Database utility/config
    ├── language_detector.py # Supreme Detection Engine (Core Logic)
    ├── main.py              # Application Entry Point
    ├── run_tests.py         # Test Runner for Language Detection
    └── test_samples.py      # Regression Test Data
💻 Installation & Setup
Prerequisites
Python 3.8+

Node.js (Optional, if required for db.js utilities)

1. Clone & Navigate
Clone the repository and move into the backend directory:

Bash

git clone <repository-url>
cd backend
2. Configure Environment
Create your environment file by copying the example:

Bash

cp .env.example .env
Open .env and fill in any required variables (e.g., Database URL, API Keys).

3. Install Dependencies
Ensure you have the required Python packages installed (FastAPI, Uvicorn, etc.):

Bash

pip install -r requirements.txt
(If you haven't created a requirements.txt yet, you likely need: pip install fastapi uvicorn python-dotenv)

4. Run the Server
Start the backend server using Uvicorn on port 3001 with hot-reloading enabled:

Bash

uvicorn main:app --reload --port 3001
The API will be available at: http://localhost:3001

🧪 Testing
To ensure the Supreme Detection Engine is accurate and the language isolation logic is working correctly, run the dedicated test suite:

Bash

python run_tests.py
This will execute:

Accuracy Phase: Verifies that language samples are correctly identified.

Isolation Phase: Ensures code samples are rejected when submitted as the wrong language.

📡 API Endpoints (Example)
GET /: Health check.

POST /detect (Hypothetical): Accepts a code snippet and returns the detected language.

🤝 Contributing
Fork the repository.

Create a feature branch (git checkout -b feature/NewHeuristic).

Commit your changes.

Run python run_tests.py to ensure no regressions.

Push to the branch and open a Pull Request.

📄 License
This project is created for educational and development purposes.

Powered by CodePercept Backend
