from typing import Any
from pydantic import BaseModel, Field

class OfferOut(BaseModel):
    id: int
    store: str
    price: float
    original_price: float
    currency: str
    availability: str
    product_url: str

class ProductOut(BaseModel):
    id: int
    title: str
    brand: str
    category: str
    image_url: str
    description: str
    specs: dict[str, Any]
    rating: float
    review_count: int
    best_price: float | None = None
    offers: list[OfferOut] = []
    match_score: float | None = None

class SearchResponse(BaseModel):
    query: str
    interpreted: dict[str, Any]
    products: list[ProductOut]
    total: int

class AlertIn(BaseModel):
    product_id: int
    target_price: float = Field(gt=0)
    email: str = ""

class WishlistIn(BaseModel):
    product_id: int
