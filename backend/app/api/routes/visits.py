from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import SiteVisit, User, VisitStatusEnum
from app.schemas.operations import VisitCreate, VisitResponse, VisitUpdate
from app.api.deps import get_current_user, get_current_admin

router = APIRouter()

@router.post("", response_model=VisitResponse)
def request_visit(visit_in: VisitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    visit = SiteVisit(
        customer_id=current_user.id,
        property_id=visit_in.property_id,
        scheduled_at=visit_in.scheduled_at,
        status=VisitStatusEnum.requested
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit

@router.get("", response_model=List[VisitResponse])
def get_customer_visits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(SiteVisit).filter(SiteVisit.customer_id == current_user.id).all()

@router.get("/{visit_id}", response_model=VisitResponse)
def get_visit(visit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    visit = db.query(SiteVisit).filter(SiteVisit.id == visit_id, SiteVisit.customer_id == current_user.id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit

@router.patch("/{visit_id}", response_model=VisitResponse)
def update_visit(visit_id: int, visit_in: VisitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    visit = db.query(SiteVisit).filter(SiteVisit.id == visit_id, SiteVisit.customer_id == current_user.id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    if visit_in.scheduled_at:
        visit.scheduled_at = visit_in.scheduled_at
        visit.status = VisitStatusEnum.rescheduling_requested
    if visit_in.customer_notes is not None:
        visit.customer_notes = visit_in.customer_notes
        
    db.commit()
    db.refresh(visit)
    return visit

@router.post("/{visit_id}/cancel", response_model=VisitResponse)
def cancel_visit(visit_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    visit = db.query(SiteVisit).filter(SiteVisit.id == visit_id, SiteVisit.customer_id == current_user.id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    visit.status = VisitStatusEnum.cancelled
    db.commit()
    db.refresh(visit)
    return visit
