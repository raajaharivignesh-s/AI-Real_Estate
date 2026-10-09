from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.session import get_db
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyResponse, PropertyListResponse
from app.db.models import Property, LandDetails, PropertyTypeEnum, AvailabilityEnum
from app.api.deps import get_current_admin

router = APIRouter()

@router.get("", response_model=PropertyListResponse)
def get_properties(
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 10,
    city: Optional[str] = None,
    property_type: Optional[PropertyTypeEnum] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    availability: Optional[AvailabilityEnum] = AvailabilityEnum.available
):
    query = db.query(Property)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    if availability:
        query = query.filter(Property.availability_status == availability)
        
    total = query.count()
    properties = query.offset((page - 1) * size).limit(size).all()
    
    return PropertyListResponse(
        items=properties,
        total=total,
        page=page,
        size=size
    )

@router.get("/featured", response_model=List[PropertyResponse])
def get_featured_properties(db: Session = Depends(get_db)):
    return db.query(Property).filter(Property.availability_status == AvailabilityEnum.available).limit(6).all()

@router.get("/locations", response_model=List[str])
def get_locations(db: Session = Depends(get_db)):
    locations = db.query(Property.city).distinct().all()
    return [loc[0] for loc in locations if loc[0]]

@router.get("/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

@router.post("", response_model=PropertyResponse)
def create_property(
    prop_in: PropertyCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    prop_data = prop_in.model_dump(exclude={"land_details"})
    prop = Property(**prop_data)
    db.add(prop)
    db.flush()
    if prop_in.land_details:
        land = LandDetails(**prop_in.land_details.model_dump(), property_id=prop.id)
        db.add(land)
    db.commit()
    db.refresh(prop)
    return prop
