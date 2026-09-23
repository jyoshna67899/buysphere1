# BuySphere — v2 Completion Guide

## Current build
This repository is a full-stack runnable MVP with:
- React + Vite frontend
- FastAPI backend
- SQLAlchemy persistence
- SQLite by default / PostgreSQL-ready
- Natural-language shopping search
- Live Google Shopping aggregation through SerpApi
- Product cards, filters, sorting and product links
- Wishlist / price-alert backend
- Product comparison API
- Fallback demo catalog

## Run locally on Windows

### Backend
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Set `SERPAPI_KEY` in `.env` to enable live shopping search.

### Frontend
Open another terminal:
```powershell
cd frontend
npm install
npm run dev
```

Then open:
http://localhost:5173

## Production completion checklist
For a true public production deployment, configure:
- PostgreSQL
- HTTPS
- JWT/session authentication
- background jobs for price refresh
- email/push notification provider
- direct retailer APIs/feeds where available
- rate limiting
- monitoring/logging
- deployment secrets
- automated tests and CI/CD

BuySphere deliberately uses provider adapters instead of claiming unrestricted scraping of every retailer. New authorized retailer/API/feed connectors can be added in `backend/app/providers.py`.
