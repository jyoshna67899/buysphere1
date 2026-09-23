from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300), index=True)
    brand: Mapped[str] = mapped_column(String(100), default="")
    category: Mapped[str] = mapped_column(String(100), default="")
    image_url: Mapped[str] = mapped_column(Text, default="")
    description: Mapped[str] = mapped_column(Text, default="")
    specs_json: Mapped[str] = mapped_column(Text, default="{}")
    rating: Mapped[float] = mapped_column(Float, default=0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    offers = relationship("Offer", back_populates="product", cascade="all, delete-orphan")

class Offer(Base):
    __tablename__ = "offers"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    store: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    original_price: Mapped[float] = mapped_column(Float, default=0)
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    availability: Mapped[str] = mapped_column(String(100), default="In stock")
    product_url: Mapped[str] = mapped_column(Text, default="#")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="offers")

class PriceHistory(Base):
    __tablename__ = "price_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    store: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Wishlist(Base):
    __tablename__ = "wishlist"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PriceAlert(Base):
    __tablename__ = "price_alerts"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    target_price: Mapped[float] = mapped_column(Float)
    email: Mapped[str] = mapped_column(String(200), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class SearchHistory(Base):
    __tablename__ = "search_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    query: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
