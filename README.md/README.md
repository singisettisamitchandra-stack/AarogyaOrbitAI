# 🌿 AarogyaOrbit AI

**AarogyaOrbit AI** is an AI-powered assistant designed to provide general health education, wellness information, and personalized grocery budget planning using a locally running language model.

## ✨ Features

- 💬 **AI Chat Assistant** — Ask questions and receive AI-generated responses.
- 🛒 **Grocery Planner** — Generate grocery plans based on budget, household size, and duration.
- 💰 **Budget Calculator** — Calculate grocery costs and compare them against a budget.
- 🤖 **Local AI Integration** — Uses Ollama with the `gemma3:1b` model.
- ⚡ **FastAPI Backend** — Provides API endpoints for the application.
- 🌐 **Web Interface** — Access the assistant through a browser.

## 🛠️ Tech Stack

- Python
- FastAPI
- Ollama
- Gemma 3 (1B)
- HTML and CSS
- SQLite

## 📁 Project Structure

```text
AarogyaOrbit-AI/
├── main.py
├── model.py
├── tools.py
├── grocery.py
├── database.py
├── SKILL.md
├── requirements.txt
├── README.md
├── .gitignore
└── static/
    └── style.css
```

*Some files may be optional or differ depending on your current project version.*

## ⚙️ Prerequisites

Before running the project, install:

1. Python 3.10 or a compatible version supported by your dependencies.
2. Git.
3. Ollama.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AarogyaOrbit-AI.git
cd AarogyaOrbit-AI
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Install and start the AI model

Install Ollama from https://ollama.com/ if it is not already installed.

Download the model:

```powershell
ollama pull gemma3:1b
```

Make sure Ollama is running.

### 5. Start the application

```powershell
uvicorn main:app --reload
```

### 6. Open the application

- **Home page:** http://127.0.0.1:8000
- **Grocery planner:** http://127.0.0.1:8000/grocery
- **API documentation:** http://127.0.0.1:8000/docs
- **Health check:** http://127.0.0.1:8000/health

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Home page |
| POST | `/api/chat` | Send a message to the AI |
| GET | `/grocery` | Grocery planner page |
| POST | `/api/grocery-plan` | Generate a grocery plan |
| POST | `/api/grocery-calculate` | Calculate grocery costs |
| GET | `/health` | Check application status |

## ⚠️ Disclaimer

AarogyaOrbit AI provides general educational information and is not a substitute for professional medical advice, diagnosis, or treatment. Grocery prices and estimates may vary.

## 👨‍💻 Project

Developed as an AI hackathon project.

Contributions and suggestions are welcome!