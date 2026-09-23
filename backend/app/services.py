import json, re
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .models import Product, Offer
from .providers import get_providers

STOP = {"the","a","an","for","with","under","below","best","good","buy","need","want","find","me","and","in","on"}

def interpret_query(q: str):
    low=q.lower()
    budget=None
    m=re.search(r"(?:under|below|less than|upto|up to)\s*[₹rs. ]*\s*([\d,]+)",low)
    if m:
        budget=float(m.group(1).replace(",",""))
    elif "₹" in q:
        m=re.search(r"₹\s*([\d,]+)",q)
        if m: budget=float(m.group(1).replace(",",""))
    category="General"
    cats={
        "laptop":["laptop","notebook","macbook"],
        "Phones":["phone","iphone","smartphone","mobile"],
        "Audio":["headphone","earbud","earphone","speaker"],
        "Footwear":["shoe","sneaker","running"],
        "Bags":["bag","backpack","rucksack"],
        "TVs":["tv","television"],
        "Kitchen":["cooker","pan","kitchen","mixer","grinder"],
        "Wearables":["watch","smartwatch","fitness band"],
    }
    for c, words in cats.items():
        if any(w in low for w in words):
            category = "Laptops" if c=="laptop" else c
            break
    tokens=[t for t in re.findall(r"[a-z0-9]+",low) if t not in STOP and len(t)>2 and not t.isdigit()]
    return {"budget":budget,"category":category,"keywords":tokens}

def score_product(p, qinfo):
    text=(p.title+" "+p.brand+" "+p.category+" "+p.description).lower()
    keys=qinfo["keywords"]
    hits=sum(1 for k in keys if k in text)
    score=min(96, 50 + hits*7)
    if qinfo["category"]!="General" and p.category.lower()==qinfo["category"].lower(): score+=12
    if qinfo["budget"]:
        best=min((o.price for o in p.offers), default=10**9)
        score += 8 if best<=qinfo["budget"] else -12
    return max(0,min(99,round(score)))

def product_dict(db,p):
    offers=db.query(Offer).filter(Offer.product_id==p.id).order_by(Offer.price.asc()).all()
    return {
        "id":p.id,"title":p.title,"brand":p.brand,"category":p.category,
        "image_url":p.image_url,"description":p.description,
        "specs":json.loads(p.specs_json or "{}"),"rating":p.rating,
        "review_count":p.review_count,
        "best_price":offers[0].price if offers else None,
        "offers":[{"id":o.id,"store":o.store,"price":o.price,"original_price":o.original_price,
                   "currency":o.currency,"availability":o.availability,"product_url":o.product_url} for o in offers]
    }

async def search(db: Session, query: str):
    qinfo=interpret_query(query)
    providers=get_providers()
    external=[]
    for provider in providers:
        external += await provider.search(query)

    terms=qinfo["keywords"]
    conditions=[]
    for t in terms[:6]:
        conditions.extend([Product.title.ilike(f"%{t}%"), Product.brand.ilike(f"%{t}%"), Product.category.ilike(f"%{t}%"), Product.description.ilike(f"%{t}%")])
    products=[]
    if conditions:
        products=db.query(Product).filter(or_(*conditions)).all()
    else:
        products=db.query(Product).all()
    # Category boost/filter is intentionally soft so generic searches still work.
    if qinfo["category"] != "General":
        matching_category=[p for p in products if p.category.lower() == qinfo["category"].lower()]
        if matching_category:
            products=matching_category
    if qinfo["budget"]:
        within=[p for p in products if min((o.price for o in p.offers), default=10**9) <= qinfo["budget"]]
        if within:
            products=within
    ranked=sorted(products, key=lambda p: score_product(p,qinfo), reverse=True)
    results=[]
    for p in ranked[:30]:
        d=product_dict(db,p)
        d["match_score"]=score_product(p,qinfo)
        results.append(d)

    # Live provider results are included as external cards. They are not persisted,
    # avoiding accidental database pollution from provider data.
    if external:
        # Live shopping results are the primary results when a live provider is enabled.
        # The local catalog is still available as a fallback when no live results are returned.
        live_results=[]
        for i,x in enumerate(external[:40]):
            live_results.append({
                "id":-100000-i,"title":x.title,"brand":x.source,"category":x.category,
                "image_url":x.image_url,"description":"Live product result from an enabled shopping provider.",
                "specs":x.specs,"rating":x.rating,"review_count":x.reviews,
                "best_price":x.price,"match_score":None,
                "offers":[{"id":-100000-i,"store":x.source,"price":x.price,
                           "original_price":x.original_price,"currency":"INR",
                           "availability":"See retailer","product_url":x.product_url}]
            })
        results = live_results
    return qinfo, results
