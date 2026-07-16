# TruthLens Local Development Setup (Hackathon Optimized)

This guide provides step-by-step instructions for running TruthLens entirely on your local machine without using Docker. This setup is highly optimized for hackathons as it avoids virtualization overhead and is easier to debug.

## Prerequisites

Before starting, ensure you have the following installed:
- Python 3.10+ (Recommended: 3.11 or 3.12)
- Node.js 18+ (Recommended: 20+)
- PostgreSQL 15+ (Install locally via `postgresql.org` or `winget install PostgreSQL.PostgreSQL`)
- Ollama (Install from `ollama.ai`)

## Step 1: Database Setup

1. Open your PostgreSQL administration tool (pgAdmin or `psql`).
2. Ensure you know the password for the root `postgres` user.
3. You do not need to create the `truthlens` database manually; our script will handle it.

## Step 2: Ollama Setup

TruthLens relies on local LLMs for AI analysis. Pull the required model:
```bash
ollama run phi3:mini
# Or, if using llama3.1
# ollama run llama3.1:8b
```
Ensure Ollama is running in the background (`ollama serve`).

## Step 3: Backend Setup

Open a terminal and navigate to the `backend` directory.

1. **Create and activate a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
Open `.env` and replace `truthlens123` with your actual PostgreSQL password. By default, Qdrant will run in `persistent` mode, saving data to `./qdrant_data`.

4. **Initialize databases:**
```bash
# Creates the PostgreSQL database
python scripts/setup_db.py

# Runs the database schema migrations
alembic upgrade head

# Creates the Qdrant collections
python scripts/setup_qdrant.py
```

5. **Seed demo data:**
```bash
python scripts/seed_admin.py
python scripts/seed_knowledge_base.py
python scripts/seed_fraud_patterns.py
```

6. **Start the backend server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
The backend is now running at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.

## Step 4: Frontend Setup

Open a **new** terminal and navigate to the `frontend` directory.

1. **Install dependencies:**
```bash
npm install
```

2. **Configure environment variables:**
Copy `.env.example` to `.env.local` (create one if it doesn't exist):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

3. **Start the frontend server:**
```bash
npm run dev
```
The frontend is now running at `http://localhost:3000`.

## Daily Usage

For everyday development, you only need to run:
1. Terminal 1 (Backend): `venv\Scripts\activate` -> `uvicorn app.main:app --reload`
2. Terminal 2 (Frontend): `npm run dev`
3. Background: Ensure PostgreSQL and Ollama are running.

## Troubleshooting

- **Authentication Errors**: Ensure `JWT_SECRET` is exactly the same in your `.env`. Clear your browser's local storage and try logging in again.
- **Database Connection Failed**: Double-check your `DATABASE_URL` in `.env` and ensure the PostgreSQL service is running in Windows Services.
- **Qdrant Errors**: If you switch from `memory` to `persistent`, you must run `setup_qdrant.py` again to initialize the new storage format.
