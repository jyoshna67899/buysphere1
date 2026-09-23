import json
from sqlalchemy.orm import Session
from .models import Product, Offer, PriceHistory

IMG = {
    "phone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80",
    "laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80",
    "headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
    "shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
    "watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
    "backpack": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
    "tv": "https://images.unsplash.com/photo-1593784991095-a205069470b6?auto=format&fit=crop&w=900&q=80",
    "kitchen": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=900&q=80",
}

SEED = [
    ("Nova X Pro 5G 256GB","Nova","Phones","phone","Premium 5G smartphone with AMOLED display and fast charging.",4.5,18200,{"storage":"256GB","ram":"12GB","network":"5G"}),
    ("PixelView 10 128GB","PixelView","Phones","phone","Clean Android experience with advanced camera system.",4.4,12100,{"storage":"128GB","ram":"8GB","network":"5G"}),
    ("ZenBook Air 14 Ryzen 7","ZenBook","Laptops","laptop","Lightweight laptop for coding, college and productivity.",4.6,8900,{"ram":"16GB","storage":"512GB SSD","processor":"Ryzen 7"}),
    ("IdeaPad Flex 5 16GB","Lenovo","Laptops","laptop","Flexible productivity laptop with 16GB RAM.",4.4,7400,{"ram":"16GB","storage":"512GB SSD","processor":"Ryzen 5"}),
    ("SonicBeat Wireless ANC","SonicBeat","Audio","headphones","Wireless over-ear headphones with active noise cancellation.",4.5,15600,{"type":"Over-ear","anc":"Yes","battery":"35 hours"}),
    ("AirWave Buds Pro","AirWave","Audio","headphones","Compact wireless earbuds with transparency mode.",4.3,9800,{"type":"TWS","anc":"Yes","battery":"30 hours"}),
    ("Runner Max 2","Stride","Footwear","shoes","Lightweight daily running shoes with cushioned sole.",4.3,5200,{"gender":"Unisex","use":"Running","closure":"Lace-up"}),
    ("Urban Trek Backpack 25L","TrailPack","Bags","backpack","Water-resistant backpack with laptop compartment.",4.6,6300,{"capacity":"25L","laptop":"15.6 inch","material":"Polyester"}),
    ("VisionMax 55 4K Smart TV","VisionMax","TVs","tv","55-inch 4K smart television with HDR support.",4.5,11200,{"screen":"55 inch","resolution":"4K","smart":"Yes"}),
    ("Chrono Fit S2","Chrono","Wearables","watch","Fitness smartwatch with heart-rate and activity tracking.",4.2,4100,{"display":"AMOLED","gps":"Yes","battery":"7 days"}),
    ("ChefPro 5L Pressure Cooker","ChefPro","Kitchen","kitchen","Stainless steel pressure cooker for everyday cooking.",4.5,3400,{"capacity":"5L","material":"Stainless steel"}),
]

STORES = ["Amazon","Flipkart","Croma","Reliance Digital"]
BASE = [24999, 21999, 58999, 52999, 4999, 3499, 2799, 1899, 42999, 3999, 2499]

def seed(db: Session):
    if db.query(Product).count():
        return
    for i, row in enumerate(SEED):
        title, brand, category, key, desc, rating, reviews, specs = row
        p = Product(title=title, brand=brand, category=category, image_url=IMG[key],
                    description=desc, specs_json=json.dumps(specs), rating=rating, review_count=reviews)
        db.add(p)
        db.flush()
        base = BASE[i]
        for j, store in enumerate(STORES):
            # Deterministic variation across stores.
            price = round(base * (1 + [0.00, 0.018, 0.045, 0.027][j]), 2)
            o = Offer(product_id=p.id, store=store, price=price, original_price=round(price*1.12,2),
                      product_url="https://www.google.com/search?q=" + title.replace(" ","+") + "+" + store.replace(" ","+"))
            db.add(o)
            for k in range(6):
                db.add(PriceHistory(product_id=p.id, store=store, price=round(price*(1+[.11,.08,.05,.03,.015,0][k]),2)))
    db.commit()
