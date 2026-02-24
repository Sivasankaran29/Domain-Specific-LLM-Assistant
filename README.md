# ⚖️ Law Chatbot — Domain-Controlled Indian Legal Information Assistant

A production-ready domain-specific AI assistant that provides **general legal information about Indian law** using **OpenRouter**, **LangChain**, **FastAPI**, **MongoDB**, and a **Streamlit ChatGPT-style UI**.

This system is designed with **strict prompt engineering, domain control, structured outputs, and refusal handling** to ensure safe and consistent responses for public users.

---

## 🚀 Overview

The Law Chatbot is an informational assistant that helps users understand:

* Indian legal concepts
* Applicable laws and sections
* High-level procedures
* General legal awareness

It **does not provide legal advice** and strictly enforces domain boundaries.

---

## 🧠 Core Features

### Domain-Specific Legal Assistant

* Focused only on Indian law
* Rejects unrelated queries
* Avoids legal advice or strategy

### Strict Prompt Engineering

* Explicit role definition
* Domain boundaries
* Tone control
* Structured JSON output
* Mandatory disclaimer
* Refusal enforcement

### Structured Output

All responses follow a fixed schema:

```json
{
  "type": "legal",
  "data": {
    "summary": "",
    "detailed_explanation": "",
    "relevant_laws": [],
    "general_process": "",
    "important_notes": "",
    "confidence_level": "",
    "disclaimer": ""
  }
}
```

Refusal format:

```json
{
  "type": "refusal",
  "data": {
    "reason": "Out of domain",
    "message": "I provide general information about Indian law only."
  }
}
```

---

## 🏗 Tech Stack

### LLM Layer

* **OpenRouter API**
* **LangChain** for orchestration and prompt control

### Backend

* FastAPI
* MongoDB (sessions, messages, summaries)
* JWT authentication
* Async architecture

### Frontend

* Streamlit
* ChatGPT-style UI
* Session history
* Smooth typing animation
* Structured rendering

---

## 🧩 Architecture

```
User → Streamlit UI
     → FastAPI backend
     → LangChain
     → OpenRouter LLM
     → Structured JSON response
     → MongoDB storage
     → UI rendering
```

---

## 🔒 Safety & Domain Control

The assistant enforces:

* Refusal of unrelated queries
* No legal advice
* No predictions or strategy
* No unsafe instructions
* Mandatory disclaimer
* Fixed response structure

This ensures consistent and safe behavior for public use.

---

## 📁 Project Structure

```
backend/
│
├── main.py
├── chat.py
├── llm.py
├── session_llm.py
├── auth.py
├── db.py
├── memory.py
├── cache.py
├── history.py
└── utils/
    └── retry.py

frontend/
└── app.py

.env
requirements.txt
README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file:

```
OPENROUTER_API_KEY=your_key
MODEL_NAME=openai/gpt-oss-20b:free
MONGODB_URI=mongodb://localhost:27017
```

---

## ▶️ Running the Project

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Start MongoDB

```
mongod
```

### 3. Start backend

```
uvicorn backend.main:app --reload
```

### 4. Start frontend

```
streamlit run frontend/app.py
```

---

## 🧪 Testing

Example legal queries:

* How to file FIR in India
* IPC section for cheating
* Property dispute process
* Divorce procedure India
* Cybercrime complaint

Unrelated queries should be refused:

* Cooking recipes
* Coding help
* Movies
* Sports

---

## 🎯 Design Principles

* Predictable output
* Domain-restricted responses
* Public-friendly language
* Safe refusal behavior
* Consistent UI experience

---

## 🔮 Future Improvements

* Legal document retrieval (RAG)
* Case law search
* Section validation layer
* Multi-model fallback
* Docker deployment
* Analytics dashboard

---

## ⚠️ Disclaimer

This system provides **general legal information about Indian law** for educational purposes only.
It does not constitute legal advice and should not replace consultation with a qualified legal professional.

---

## 📜 License

Internal / Educational Use.
