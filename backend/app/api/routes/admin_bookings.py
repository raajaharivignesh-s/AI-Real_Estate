from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import Booking, User
from app.schemas.operations import BookingResponse, BookingUpdate
from app.api.deps import get_current_admin

router = APIRouter()

@router.get("", response_model=List[BookingResponse])
def admin_get_bookings(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return db.query(Booking).all()

@router.patch("/{booking_id}", response_model=BookingResponse)
def admin_update_booking(booking_id: int, booking_in: BookingUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking_in.status:
        booking.status = booking_in.status
    if booking_in.payment_status:
        booking.payment_status = booking_in.payment_status
    db.commit()
    db.refresh(booking)
    return booking
