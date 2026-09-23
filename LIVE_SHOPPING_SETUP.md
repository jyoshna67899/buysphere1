# BuySphere live shopping connection

BuySphere now has a live Google Shopping connector.

## 1. Create a SerpApi account and API key

Create an account at SerpApi and copy your private API key.

## 2. Configure the backend

Inside `backend`, create a file named `.env`:

```env
USE_LIVE_SEARCH=true
SERPAPI_KEY=PASTE_YOUR_KEY_HERE
SHOPPING_COUNTRY=in
SHOPPING_LANGUAGE=en
SHOPPING_LOCATION=
DATABASE_URL=sqlite:///./buysphere.db
CORS_ORIGINS=http://localhost:5173
```

Never put the API key in React/frontend code and never commit `.env` to GitHub.

## 3. Install and run

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then:

```bash
cd frontend
npm install
npm run dev
```

Open:

`http://localhost:5173`

## 4. Test live search

Try:

- `iphone 17 256gb`
- `laptop for coding under ₹60000`
- `wireless headphones under ₹5000`
- `running shoes for men`
- `5 litre pressure cooker`

The backend sends the natural-language query to Google Shopping through SerpApi. The returned shopping records include retailer/source, price, ratings, review counts, product links and thumbnails. BuySphere renders those live records as product cards.

## 5. How the "many sites" part works

BuySphere does not directly scrape every retailer one-by-one. The Google Shopping connector can return offers from multiple shopping sources for a query. This gives BuySphere a broad multi-retailer search layer.

For a production deployment, add direct authorized retailer APIs, affiliate feeds, or product feeds as additional adapters in:

`backend/app/providers.py`

Each adapter should return the same `ExternalProduct` structure.

## 6. If live search returns no products

Check:

1. `SERPAPI_KEY` is correct.
2. `USE_LIVE_SEARCH=true`.
3. Backend was restarted after changing `.env`.
4. Your SerpApi account has available searches.
5. The backend can reach `serpapi.com`.

The app intentionally falls back to the built-in catalog if the live provider fails, so the UI remains demonstrable.

## Security

- Do not share your API key in screenshots, GitHub, or the frontend.
- Use environment variables on deployment.
- Add rate limiting and caching before public launch.
- Respect the terms and access rules of each data provider.
