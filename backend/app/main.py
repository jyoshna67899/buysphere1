from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .db import Base, engine, get_db
from .models import Product, Offer, PriceHistory, Wishlist, PriceAlert, SearchHistory
from .schemas import SearchResponse, ProductOut, AlertIn, WishlistIn
from .catalog import seed
from .services import search, product_dict

app=FastAPI(title="BuySphere AI API", version="1.0.0")

origins=[x.strip() for x in __import__("os").getenv("CORS_ORIGINS","http://localhost:5173").split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db=next(get_db())
    try: seed(db)
    finally: db.close()


@app.post("/api/compare")
def compare_products(product_ids: list[int], db: Session = Depends(get_db)):
    """Compare locally stored products by ID."""
    if not product_ids:
        return {"products": []}
    products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    result = []
    for p in products:
        offers = db.query(Offer).filter(Offer.product_id == p.id).all()
        result.append({
            "id": p.id,
            "title": p.title,
            "brand": p.brand,
            "category": p.category,
            "image_url": p.image_url,
            "rating": p.rating,
            "reviews": p.review_count,
            "offers": [
                {
                    "store": o.store,
                    "price": o.price,
                    "old_price": o.original_price,
                    "url": o.product_url,
                    "availability": o.availability,
                } for o in offers
            ],
        })
    return {"products": result}

@app.get("/api/health")
def health():
    return {"status":"ok","service":"BuySphere AI"}

@app.get("/api/search", response_model=SearchResponse)
async def search_products(q: str=Query(..., min_length=1), db: Session=Depends(get_db)):
    info, products=await search(db,q)
    db.add(SearchHistory(query=q)); db.commit()
    return {"query":q,"interpreted":info,"products":products,"total":len(products)}

@app.get("/api/products/{product_id}")
def get_product(product_id:int, db:Session=Depends(get_db)):
    p=db.get(Product,product_id)
    if not p: raise HTTPException(404,"Product not found")
    return product_dict(db,p)

@app.get("/api/products/{product_id}/history")
def price_history(product_id:int, db:Session=Depends(get_db)):
    rows=db.query(PriceHistory).filter(PriceHistory.product_id==product_id).order_by(PriceHistory.recorded_at.asc()).all()
    return [{"store":x.store,"price":x.price,"recorded_at":x.recorded_at.isoformat()} for x in rows]

@app.get("/api/wishlist")
def wishlist(db:Session=Depends(get_db)):
    rows=db.query(Wishlist).order_by(desc(Wishlist.created_at)).all()
    out=[]
    for r in rows:
        p=db.get(Product,r.product_id)
        if p: out.append(product_dict(db,p))
    return out

@app.post("/api/wishlist")
def add_wishlist(body:WishlistIn, db:Session=Depends(get_db)):
    if body.product_id<0: raise HTTPException(400,"Live results cannot be saved until opened as a retailer item.")
    if not db.get(Product,body.product_id): raise HTTPException(404,"Product not found")
    existing=db.query(Wishlist).filter(Wishlist.product_id==body.product_id).first()
    if not existing:
        db.add(Wishlist(product_id=body.product_id)); db.commit()
    return {"ok":True}

@app.delete("/api/wishlist/{product_id}")
def remove_wishlist(product_id:int, db:Session=Depends(get_db)):
    db.query(Wishlist).filter(Wishlist.product_id==product_id).delete()
    db.commit()
    return {"ok":True}

@app.post("/api/alerts")
def add_alert(body:AlertIn, db:Session=Depends(get_db)):
    if body.product_id<0: raise HTTPException(400,"Live result alerting requires persistent retailer data.")
    if not db.get(Product,body.product_id): raise HTTPException(404,"Product not found")
    db.add(PriceAlert(product_id=body.product_id,target_price=body.target_price,email=body.email))
    db.commit()
    return {"ok":True,"message":"Price alert created"}

@app.get("/api/alerts")
def get_alerts(db:Session=Depends(get_db)):
    rows=db.query(PriceAlert).order_by(desc(PriceAlert.created_at)).all()
    out=[]
    for a in rows:
        p=db.get(Product,a.product_id)
        if p:
            out.append({"id":a.id,"product_id":a.product_id,"product_title":p.title,"target_price":a.target_price,"email":a.email,"active":a.active,"created_at":a.created_at.isoformat()})
    return out

@app.delete("/api/alerts/{alert_id}")
def delete_alert(alert_id:int, db:Session=Depends(get_db)):
    row=db.get(PriceAlert,alert_id)
    if not row: raise HTTPException(404,"Alert not found")
    db.delete(row); db.commit()
    return {"ok":True}

@app.get("/api/history")
def search_history(db:Session=Depends(get_db)):
    rows=db.query(SearchHistory).order_by(desc(SearchHistory.created_at)).limit(20).all()
    return [{"query":r.query,"created_at":r.created_at.isoformat()} for r in rows]
