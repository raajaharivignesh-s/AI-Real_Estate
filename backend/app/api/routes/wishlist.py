from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import Wishlist, Property, User
from app.api.deps import get_current_user
from app.schemas.property import PropertyResponse

router = APIRouter()

@router.get("", response_model=List[PropertyResponse])
def get_wishlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wishlist_items = db.query(Wishlist).filter(Wishlist.customer_id == current_user.id).all()
    
    # Need to fetch the actual property records since relationship might not be loaded if not defined correctly in model
    # Wait, the model doesn't have a property relationship on Wishlist explicitly. Let's query properties manually or update model.
    property_ids = [item.property_id for item in wishlist_items]
    if not property_ids:
        return []
        
    properties = db.query(Property).filter(Property.id.in_(property_ids)).all()
    return properties

@router.post("/{property_id}")
def add_to_wishlist(property_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
        
    existing = db.query(Wishlist).filter(Wishlist.customer_id == current_user.id, Wishlist.property_id == property_id).first()
    if existing:
        return {"message": "Already in wishlist"}
        
    wishlist_item = Wishlist(customer_id=current_user.id, property_id=property_id)
    db.add(wishlist_item)
    db.commit()
    return {"message": "Added to wishlist"}

@router.delete("/{property_id}")
def remove_from_wishlist(property_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Wishlist).filter(Wishlist.customer_id == current_user.id, Wishlist.property_id == property_id).first()
    if item:
        db.delete(item)
        db.commit()
    return {"message": "Removed from wishlist"}
