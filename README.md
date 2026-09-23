# BuySphere AI

A full-stack, multi-source shopping discovery and comparison platform.

## What it does

- Natural-language product search
- Multi-source product aggregation through provider adapters
- Product images, prices, ratings, offers and specifications
- Cross-store comparison
- AI-style requirement extraction and product matching
- Product detail pages
- Price history
- Wishlist
- Search history
- Price alerts
- Responsive React UI
- FastAPI REST backend
- SQLite by default; PostgreSQL-ready through DATABASE_URL

> Important: BuySphere cannot legally/technically scrape every e-commerce website automatically. The production design uses permitted APIs, feeds, affiliate/product-data providers, and retailer integrations. The included demo provider makes the project runnable immediately. Add real provider credentials to enable live shopping data.

## Stack

Frontend: React + Vite + CSS
Backend: Python + FastAPI + SQLAlchemy
Database: SQLite by default
Optional live provider: SerpAPI Google Shopping

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API: http://localhost:8000
Swagger: http://localhost:8000/docs

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

The frontend proxies `/api` to the FastAPI backend.

## Live multi-retailer shopping search

The project includes a live Google Shopping connector through SerpApi. Google Shopping results can contain offers from multiple shopping sources and include fields such as title, price, source, rating, reviews, thumbnail and product link.

Create `backend/.env`:

```env
USE_LIVE_SEARCH=true
SERPAPI_KEY=your_key_here
SHOPPING_COUNTRY=in
SHOPPING_LANGUAGE=en
SHOPPING_LOCATION=
```

Keep the key only on the backend. See `LIVE_SHOPPING_SETUP.md` for the complete setup.

## Included in the completed build

- Working search, filtering and sorting
- Natural-language budget/category extraction
- Demo catalog that works without an API key
- Optional live Google Shopping provider
- Product detail modal and offer list
- Side-by-side comparison for up to four products
- Wishlist
- Search history
- Price-alert management
- Responsive desktop/mobile UI
- FastAPI health endpoint and Swagger docs

## Important for live production data

Live retailer data depends on the external provider account and the retailer/provider permissions. The application is fully runnable without those credentials using its built-in catalog; adding `SERPAPI_KEY` switches on live shopping aggregation. For a public production deployment, add additional authorized retailer/feed adapters and a notification service for automated alerts.
