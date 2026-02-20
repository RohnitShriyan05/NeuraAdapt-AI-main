# NeuraAdapt-AI

AI-powered attention analysis for video learning with engagement scoring, confusion detection, and automated notes.

## Features

- MediaPipe-based gaze and head pose tracking
- Engagement scoring and confusion events
- Heatmaps and timestamped notes
- Flask API + Next.js dashboard

## Deployment

### Local (Docker)

1. Copy env files and update values as needed:

```bash
cp .env.example .env
cp client/.env.example client/.env
```

2. Start the full stack:

```bash
docker compose up --build
```

3. Open the apps:

- API: http://localhost:5000/health
- Web: http://localhost:3000

### Local (manual)

1. Backend:

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/neuraadapt
python main.py
```

2. Frontend:

```bash
cd client
npm install
npm run dev
```

## Configuration

- `DATABASE_URL`: Postgres connection string
- `STORAGE_BACKEND`: `local` or `s3`
- `STORAGE_PATH`: local output directory
- `GEMINI_API_KEY`: required for flashcard generation

## API

- `POST /analyze` (multipart form-data with `video`)
- `GET /sessions/{id}`
- `GET /health`
