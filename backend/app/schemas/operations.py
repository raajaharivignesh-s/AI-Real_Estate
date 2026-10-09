from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.db.models import VisitStatusEnum, BookingStatusEnum, SupportPriorityEnum, SupportStatusEnum

class VisitCreate(BaseModel):
    property_id: int
    scheduled_at: datetime

class VisitUpdate(BaseModel):
    scheduled_at: Optional[datetime] = None
    status: Optional[VisitStatusEnum] = None
    customer_notes: Optional[str] = None
    admin_notes: Optional[str] = None

class VisitResponse(BaseModel):
    id: int
    customer_id: int
    property_id: int
    scheduled_at: datetime
    status: VisitStatusEnum
    customer_notes: Optional[str] = None
    admin_notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class BookingResponse(BaseModel):
    id: int
    customer_id: int
    property_id: int
    booking_reference: str
    status: BookingStatusEnum
    payment_status: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class BookingUpdate(BaseModel):
    status: Optional[BookingStatusEnum] = None
    payment_status: Optional[str] = None

class SupportCreate(BaseModel):
    property_id: Optional[int] = None
    booking_id: Optional[int] = None
    visit_id: Optional[int] = None
    category: str
    subject: str
    description: str
    priority: Optional[SupportPriorityEnum] = SupportPriorityEnum.medium

class SupportUpdate(BaseModel):
    status: Optional[SupportStatusEnum] = None
    priority: Optional[SupportPriorityEnum] = None
    resolution_notes: Optional[str] = None

class SupportResponse(BaseModel):
    id: int
    customer_id: int
    property_id: Optional[int] = None
    booking_id: Optional[int] = None
    visit_id: Optional[int] = None
    category: str
    subject: str
    description: str
    priority: SupportPriorityEnum
    status: SupportStatusEnum
    resolution_notes: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
