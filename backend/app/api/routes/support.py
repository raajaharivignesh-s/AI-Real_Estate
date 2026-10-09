from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import SupportRequest, User
from app.schemas.operations import SupportCreate, SupportResponse, SupportUpdate
from app.api.deps import get_current_user, get_current_admin

router = APIRouter()

@router.post("/requests", response_model=SupportResponse)
def create_support_request(req_in: SupportCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    req = SupportRequest(
        customer_id=current_user.id,
        **req_in.model_dump()
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

@router.get("/requests", response_model=List[SupportResponse])
def get_customer_support_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(SupportRequest).filter(SupportRequest.customer_id == current_user.id).all()

@router.get("/requests/{request_id}", response_model=SupportResponse)
def get_support_request(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    req = db.query(SupportRequest).filter(SupportRequest.id == request_id, SupportRequest.customer_id == current_user.id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@router.patch("/requests/{request_id}", response_model=SupportResponse)
def update_support_request(request_id: int, req_in: SupportUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    req = db.query(SupportRequest).filter(SupportRequest.id == request_id, SupportRequest.customer_id == current_user.id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    # Customers can only update certain fields, but for simplicity, we just allow the update struct
    if req_in.status:
        req.status = req_in.status
    if req_in.resolution_notes is not None:
        req.resolution_notes = req_in.resolution_notes
    db.commit()
    db.refresh(req)
    return req
