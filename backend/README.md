# 🚀 CodePercept

> **AI‑Powered Multi‑Language Code Intelligence Platform**
> Detect • Analyze • Explain • Fix Code — Automatically

---

## 🌟 Overview

**CodePercept** is an AI code analysis platform designed to **understand, validate, explain, and correct source code across 20+ programming languages**. It goes beyond syntax checking by providing **line-by-line explanations, intelligent error detection, language mismatch detection, and full auto-fixes** — all powered by modern AI models.

🔴 **Live Demo**: [https://code-percept.onrender.com/](https://code-percept.onrender.com/)

This project demonstrates **real-world engineering depth**, **AI integration**, and **production-ready backend architecture**, making it ideal for **top-tier software roles**.

---

## 🎯 Why CodePercept?

Most code tools either *compile* or *lint*. **CodePercept actually understands code.**

✔ Explains *why* code works
✔ Pinpoints *exact lines* causing issues
✔ Detects *wrong language selection* automatically
✔ Produces *fully corrected, runnable code*

---

## ✨ Key Features

### 🧠 Intelligent Language Detection

* Automatically detects the **actual programming language** of the pasted code
* Warns users if the selected language **does not match** the detected one

### 🧩 Line‑by‑Line Code Explanation

* Explains **each line of correct code** in a structured, readable format
* Output style inspired by **GeeksForGeeks / W3Schools** standards

### 🚨 Precise Error Detection

* Identifies **syntax errors, logical errors, semantic issues**
* Highlights **exact line numbers** responsible for failures
* Clearly explains **what is wrong and why**

### 🛠️ Full Auto‑Fix Engine

* Generates a **complete corrected version** of the code
* Preserves original intent while fixing errors
* Produces **clean, production‑ready output**

### 🌐 Multi‑Language Support (20+)

* C, C++, Java, Python, JavaScript, TypeScript
* Go, Rust, Kotlin, Swift, PHP, Ruby
* SQL, Bash, HTML/CSS and more

### ⚡ FastAPI‑Powered Backend

* High‑performance Python backend using **FastAPI**
* Clean REST APIs for analysis and fixes
* Designed for **scalability and modularity**

### 🔐 Safe & Isolated Analysis

* No direct execution of user code
* Secure prompt handling and validation

---

## 🏗️ System Architecture

```text
Frontend (HTML/CSS/JS)
        │
        ▼
FastAPI Backend (Python)
        │
        ├── Language Detection Engine
        ├── Line Analyzer & Error Locator
        ├── AI Explanation Engine (Gemini)
        └── Auto‑Fix Generator
```

---

## 🧑‍💻 Tech Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript

### Backend

* Python 3.x
* FastAPI
* Pydantic
* SQLite

### AI / Intelligence

* Google Gemini API
* Custom Prompt Engineering
* Rule‑based + AI hybrid analysis

---

## 📂 Project Structure

```text
CodePercept/
│
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── gemini_client.py     # AI interaction layer
│   ├── language_detector.py # Language detection logic
│   ├── utils/
│   │   ├── line_numbers.py
│   │   ├── json_extract.py
│   │   └── prompt_loader.py
│   └── database.db
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md
```

---

## 🌍 Live Deployment

🚀 **Production URL**: [https://code-percept.onrender.com/](https://code-percept.onrender.com/)

* Fully deployed full-stack application
* Backend hosted with FastAPI
* Frontend served with real-time API interaction
* Publicly accessible for recruiters & reviewers

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/aayushthakur300/CodePercept.git
cd CodePercept
```

### 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3️⃣ Frontend

Open `frontend/index.html` in your browser

---

## 🎯 Recruiter-Ready Highlights

* Live, production-hosted project (no localhost demos)
* Real-world AI integration with strict validation
* Clean backend architecture using FastAPI
* Multi-language intelligence beyond static analysis

---

## 📌 Use Cases

* 🧑‍🎓 Students learning programming
* 💼 Interview preparation & code review
* 🧪 Debugging multi‑language snippets
* 🏢 AI‑assisted developer tooling

---

## 🧠 What Makes This Special?

* Real‑world **AI + Backend integration**
* Clean API‑driven design
* Practical developer problem solving
* Demonstrates **systems thinking**, not just CRUD

---

## 🔮 Future Enhancements

* Docker sandbox execution
* User authentication & usage billing
* Code complexity & performance analysis
* Cross‑language code translation
* Cloud deployment (AWS/GCP)

---

## 👤 Author

**Aayush Thakur**
Aspiring Software Engineer | AI & Backend Developer

🔗 GitHub: [https://github.com/aayushthakur300](https://github.com/aayushthakur300)

---

## ⭐ If you like this project

Give it a **star ⭐** — it helps a lot and motivates future improvements!
