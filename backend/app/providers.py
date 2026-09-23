
import os, re, httpx
from dataclasses import dataclass

@dataclass
class ExternalProduct:
    title: str
    source: str
    price: float
    original_price: float
    image_url: str
    rating: float
    reviews: int
    product_url: str
    specs: dict
    category: str
    delivery: str = ""

class Provider:
    name = "base"
    async def search(self, query: str) -> list[ExternalProduct]:
        return []

class SerpAPIProvider(Provider):
    """
    Live Google Shopping connector.
    Google Shopping aggregates offers from many retailers, so one query can
    return results from multiple shopping sources.
    """
    name = "google_shopping"

    async def search(self, query: str) -> list[ExternalProduct]:
        key = os.getenv("SERPAPI_KEY")
        if not key:
            return []

        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": key,
            "gl": os.getenv("SHOPPING_COUNTRY", "in"),
            "hl": os.getenv("SHOPPING_LANGUAGE", "en"),
            "location": os.getenv("SHOPPING_LOCATION", ""),
        }
        params = {k: v for k, v in params.items() if v}

        try:
            async with httpx.AsyncClient(timeout=25) as client:
                response = await client.get("https://serpapi.com/search.json", params=params)
                response.raise_for_status()
                data = response.json()

            results = data.get("shopping_results", [])
            out = []

            for item in results:
                price = item.get("extracted_price")
                if price is None:
                    raw = str(item.get("price", ""))
                    match = re.search(r"[\d,]+(?:\.\d+)?", raw)
                    price = float(match.group(0).replace(",", "")) if match else None
                if price is None:
                    continue

                original = item.get("extracted_old_price") or item.get("extracted_original_price") or price

                out.append(
                    ExternalProduct(
                        title=item.get("title", "Product"),
                        source=item.get("source", "Shopping source"),
                        price=float(price),
                        original_price=float(original),
                        image_url=item.get("thumbnail") or item.get("serpapi_thumbnail") or "",
                        rating=float(item.get("rating") or 0),
                        reviews=int(item.get("reviews") or 0),
                        # SerpApi's Google Shopping result commonly exposes
                        # product_link; fall back to link where available.
                        product_url=item.get("product_link") or item.get("link") or "#",
                        specs={
                            "delivery": item.get("delivery", ""),
                            "condition": item.get("second_hand_condition", ""),
                        },
                        category="Live result",
                        delivery=str(item.get("delivery", "")),
                    )
                )

            return out

        except Exception:
            # The local catalog remains available if the live provider has
            # a timeout, quota problem, malformed response, or no key.
            return []

def get_providers():
    if os.getenv("USE_LIVE_SEARCH", "false").lower() == "true":
        return [SerpAPIProvider()]
    return []
