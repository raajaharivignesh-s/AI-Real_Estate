from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import SupportRequest, User
from app.schemas.operations import SupportResponse, SupportUpdate
from app.api.deps import get_current_admin

router = APIRouter()

@router.get("/requests", response_model=List[SupportResponse])
def admin_get_support_requests(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return db.query(SupportRequest).all()

@router.patch("/requests/{request_id}", response_model=SupportResponse)
def admin_update_support_request(request_id: int, req_in: SupportUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    req = db.query(SupportRequest).filter(SupportRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req_in.status:
        req.status = req_in.status
    if req_in.priority:
        req.priority = req_in.priority
    if req_in.resolution_notes is not None:
        req.resolution_notes = req_in.resolution_notes
    db.commit()
    db.refresh(req)
    return req
