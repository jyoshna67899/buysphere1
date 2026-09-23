import React from 'react'
import { Heart, ExternalLink, GitCompareArrows, Bell, Star, Store, Truck } from 'lucide-react'

const money=(n)=>n==null?'—':new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format(n)

export default function ProductCard({product,liked,onWishlist,onCompare,onAlert,onDetails}){
  const discount=product.best_price && product.offers?.[0]?.original_price>product.best_price
    ? Math.round((1-product.best_price/product.offers[0].original_price)*100):0
  const live=product.id<0
  return <article className="product-card">
    <div className="image-wrap">
      <img src={product.image_url || 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=900&q=80'} alt={product.title} onError={e=>{e.currentTarget.src='https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=900&q=80'}}/>
      <button className={`icon-btn ${liked?'liked':''}`} onClick={()=>onWishlist(product)} aria-label="Wishlist"><Heart size={18} fill={liked?'currentColor':'none'}/></button>
      {product.match_score!=null && <span className="match">{product.match_score}% MATCH</span>}
      {live && <span className="live-pill">LIVE</span>}
    </div>
    <div className="card-body">
      <div className="eyebrow"><Store size={12}/> {product.brand || product.offers?.[0]?.store || 'Shopping source'}</div>
      <h3 title={product.title}>{product.title}</h3>
      <div className="rating"><Star size={13} fill="currentColor"/> {product.rating?product.rating.toFixed(1):'New'} <span>({(product.review_count||0).toLocaleString('en-IN')})</span></div>
      <div className="price">{money(product.best_price)}</div>
      <div className="mini-row"><Truck size={12}/> {product.offers?.[0]?.availability || 'Check retailer'} {discount>0&&<b> · {discount}% off</b>}</div>
      <div className="actions">
        <button className="secondary" onClick={()=>onDetails(product)}>Details</button>
        <button className="secondary" onClick={()=>onCompare(product)}><GitCompareArrows size={14}/> Compare</button>
        <button className="secondary" onClick={()=>onAlert(product)} title="Price alert"><Bell size={14}/></button>
      </div>
      <a className="deal" href={product.offers?.[0]?.product_url || '#'} target="_blank" rel="noreferrer">View deal <ExternalLink size={13}/></a>
    </div>
  </article>
}
