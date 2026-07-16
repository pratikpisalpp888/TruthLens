<div align="center">

https://github.com/pratikpisalpp888/TruthLens/raw/main/assets/VN20260715_193229.mp4

<br/><br/>

<img src="https://img.shields.io/badge/Built_for-Canara_Bank_SuRaksha_Hackathon-yellow?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJMMiAyMmgyMEwxMiAyeiIgZmlsbD0iI2ZmZiIvPjwvc3ZnPg==" />
&nbsp;
<img src="https://img.shields.io/badge/Status-Live_Demo-brightgreen?style=for-the-badge&logo=vercel" />
&nbsp;
<img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" />

<br/><br/>

<h1>🔍 TruthLens</h1>
<h3>AI-Powered Loan Document Fraud Detection — 90 Seconds. Court-Ready Evidence.</h3>

<p>Five specialized AI agents. Seven intelligence layers. Completely offline. Built for Indian Banking.</p>

</div>

---

## 🎯 What is TruthLens?

TruthLens is an enterprise-grade, **fully offline** multi-agent AI system designed for Indian financial institutions to detect loan document fraud. It replaces days of manual underwriting with a **90-second autonomous AI pipeline** that produces **court-ready, immutable PDF reports** — grounded in actual RBI regulations.

> **Built for the Canara Bank SuRaksha Hackathon** — transforming how credit officers detect financial fraud.

---

## ✨ Core Innovations

| Feature | What it does |
|---|---|
| 🧮 **Benford's Law Analysis** | Mathematically detects fabricated bank statements & ITRs using digit frequency anomalies |
| 🧬 **Fraud DNA** | Generates a unique fraud signature and cross-references it against a Qdrant vector database of known fraud patterns |
| 🕸️ **GraphRAG Network** | Maps relationships across cases — IP addresses, PANs, shared devices — to detect organized fraud rings |
| 📜 **Corrective RAG (CRAG)** | Zero hallucinations. Every AI decision is grounded in live-retrieved RBI regulations and KYC guidelines |
| 🔬 **ELA Pixel Forensics** | Error Level Analysis detects digital tampering, photoshopping, and document splicing at the pixel level |
| 📊 **ITR Deep Analysis** | Parses complex tax returns, validates digital signatures, and flags income vs. bank deposit inconsistencies |
| 🔒 **AES-256 Encryption** | All documents encrypted at rest. Local Ollama LLM means **zero PII ever leaves the bank's servers** |

---

## 🤖 The 5-Agent Pipeline

```
📄 Documents Uploaded
        │
        ▼
┌─────────────────┐    ┌──────────────────┐    ┌───────────────────┐
│  1. Classifier  │───▶│  2. Forensic     │───▶│  3. CrossRef      │
│  Identify docs  │    │  ELA + Benford's │    │  Cross-validate   │
└─────────────────┘    └──────────────────┘    └───────────────────┘
                                                        │
                              ┌─────────────────────────┘
                              ▼
                 ┌──────────────────────┐    ┌────────────────────┐
                 │  4. Compliance       │───▶│  5. Decision       │
                 │  RBI + CRAG + DPDP   │    │  Risk Score 0-100  │
                 └──────────────────────┘    └────────────────────┘
                                                        │
                                                        ▼
                                             📑 Court-Ready Report
```

---

## 🛠️ Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-purple?style=flat-square)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=flat-square)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-red?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white)

### Frontend
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=nextdotjs)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Tailwind](https://img.shields.io/badge/TailwindCSS-3-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Framer Motion](https://img.shields.io/badge/Framer_Motion-Animations-pink?style=flat-square)

### AI / ML
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-Embeddings-orange?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-Forensics-5C3EE8?style=flat-square&logo=opencv)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-OCR-green?style=flat-square)
![spaCy](https://img.shields.io/badge/spaCy-NER-09A3D5?style=flat-square)

---

## ⚡ Quick Start

### Prerequisites

Make sure you have the following installed:
- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Ollama](https://ollama.ai/) (for local LLM)

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pratikpisalpp888/TruthLens.git
cd TruthLens
```

### 2️⃣ Set Up Environment Variables

```bash
cp .env.example .env
# Open .env and fill in your configuration values
```

### 3️⃣ Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python scripts/setup_db.py

# Seed the knowledge base
python scripts/seed_knowledge_base.py
python scripts/seed_fraud_patterns.py
python scripts/seed_admin.py

# Start the backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will be live at: **http://localhost:8000**
API Docs at: **http://localhost:8000/docs**

---

### 4️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be live at: **http://localhost:3000**

---

### 5️⃣ Set Up Local LLM (Ollama)

```bash
# Install Ollama from https://ollama.ai then run:
ollama pull phi3:mini
ollama serve
```

---

### 6️⃣ Docker (All-in-One)

```bash
# From the project root
docker-compose up --build
```

---

## 📁 Project Structure

```
TruthLens/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── agents/             # 5 LangGraph AI agents
│   │   ├── extractors/         # Document extractors (ITR, PAN, etc.)
│   │   ├── forensics/          # ELA, Benford's, pixel analysis
│   │   ├── rag/                # CRAG + GraphRAG implementation
│   │   ├── services/           # Business logic layer
│   │   └── routers/            # FastAPI route handlers
│   ├── scripts/                # DB seeding & setup scripts
│   └── requirements.txt
│
├── frontend/                   # Next.js 14 TypeScript frontend
│   ├── app/                    # Next.js App Router pages
│   │   ├── (public)/           # Landing, login, about pages
│   │   └── (protected)/        # Dashboard, cases, reports
│   ├── components/
│   │   ├── landing/            # Landing page sections
│   │   └── ui/                 # Reusable UI components
│   └── stores/                 # Zustand state management
│
├── .env.example                # Environment variable template
├── docker-compose.yml          # Full stack Docker setup
└── README.md
```

---

## 🔐 Default Login Credentials

> ⚠️ Change these immediately in production via your `.env` file.

| Field | Value |
|---|---|
| **Email** | `admin@canarabank.com` |
| **Password** | Set in your `.env` as `ADMIN_PASSWORD` |



## 🏆 Hackathon

This project was built for the **Canara Bank SuRaksha Hackathon**, targeting the problem of rising sophisticated loan document fraud in the Indian banking ecosystem.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <strong>Built with ❤️ for Indian Banking — TruthLens, Detecting the Unseen.</strong>
</div>
