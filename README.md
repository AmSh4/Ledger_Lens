# LedgerLens – Tamper‑Evident Research Notebook

A local‑first, tamper‑evident notebook for experiments, research, and lab logs.
Each entry is chained with cryptographic hashes (like a mini blockchain), so any edit breaks the chain and shows as **tampered**. Attach files, tag entries, verify integrity, and export safely.

## Why this is recruiter‑attracting
- **Rare but useful**: tamper‑evident logging is common in regulated industries but uncommon in student projects.
- **Complex but doable**: clear FastAPI backend + React/Tailwind frontend + SQLite + hashing chain + tests + Docker + CI.
- **Local-first privacy**: runs entirely on your machine; no cloud required.

---

## Features
- Append‑only journal entries (title, content, tags).
- Cryptographic chaining: `current_hash = SHA256(prev_hash + content_hash + timestamp)`.
- File attachments with SHA256 fingerprinting.
- Integrity verification endpoint and visual badge in UI.
- Search/filter by tags/title.
- Export selected entries to signed JSON.
- Dockerized dev and prod.
- Unit tests for the integrity service.
- GitHub Actions CI (lint + tests).

---

## Quick Start (Dev)
### Requirements
- Python 3.10+
- Node 18+ and npm
- (Optional) Docker

### 1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The API will be at `http://localhost:8000` with docs at `/docs`.

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```
The app will be at `http://localhost:5173` (Vite).

### 3) Docker Compose (optional, one command)
```bash
docker compose up --build
```

---

## Project Structure
```
LedgerLens/
  backend/
    app/
      main.py
      db.py
      models.py
      schemas.py
      routers/
        entries.py
      services/
        integrity.py
        storage.py
      security/
        keys.py
      tests/
        test_integrity.py
    requirements.txt
    Dockerfile
  frontend/
    index.html
    package.json
    vite.config.ts
    postcss.config.js
    tailwind.config.js
    src/
      main.tsx
      App.tsx
      styles.css
      lib/api.ts
      components/
        EntryForm.tsx
        EntryList.tsx
        VerifyBadge.tsx
  docker-compose.yml
  scripts/
    dev.sh
    seed.py
  .github/workflows/ci.yml
  LICENSE
```

---

## Production build
```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend && npm ci && npm run build && npm run preview
```

---

## Notes
- Entries are **append‑only**; editing creates a new entry linked to the previous.
- Attachments are stored under `backend/app/storage/` and hashed.
- Exported JSON includes a signature placeholder; see `security/keys.py` to wire Ed25519 signing if desired.
- For demo, auth is open; integrate JWT in `security/keys.py` if needed.
