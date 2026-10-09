from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from app.db.models import PropertyTypeEnum, AvailabilityEnum, LegalVerificationEnum

class LandDetailsBase(BaseModel):
    plot_area_sqft: float
    plot_length_ft: Optional[float] = None
    plot_width_ft: Optional[float] = None
    road_access: Optional[str] = None
    land_use_type: Optional[str] = None
    survey_reference: Optional[str] = None
    legal_verification_status: Optional[LegalVerificationEnum] = None
    additional_notes: Optional[str] = None

class PropertyBase(BaseModel):
    title: str
    description: str
    property_type: PropertyTypeEnum
    price: float
    city: str
    locality: str
    address: str
    area_sqft: float
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    amenities: Optional[List[str]] = []
    image_urls: Optional[List[str]] = []
    availability_status: AvailabilityEnum = AvailabilityEnum.available

class PropertyCreate(PropertyBase):
    land_details: Optional[LandDetailsBase] = None

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    availability_status: Optional[AvailabilityEnum] = None

class LandDetailsResponse(LandDetailsBase):
    id: int
    property_id: int
    model_config = ConfigDict(from_attributes=True)

class PropertyResponse(PropertyBase):
    id: int
    land_details: Optional[LandDetailsResponse] = None
    model_config = ConfigDict(from_attributes=True)

class PropertyListResponse(BaseModel):
    items: List[PropertyResponse]
    total: int
    page: int
    size: int

class WishlistResponse(BaseModel):
    id: int
    property: PropertyResponse
    model_config = ConfigDict(from_attributes=True)
