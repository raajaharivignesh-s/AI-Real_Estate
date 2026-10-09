from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models import SiteVisit, User
from app.schemas.operations import VisitResponse, VisitUpdate
from app.api.deps import get_current_admin

router = APIRouter()

@router.get("", response_model=List[VisitResponse])
def admin_get_visits(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    return db.query(SiteVisit).all()

@router.patch("/{visit_id}", response_model=VisitResponse)
def admin_update_visit(visit_id: int, visit_in: VisitUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    visit = db.query(SiteVisit).filter(SiteVisit.id == visit_id).first()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    if visit_in.status:
        visit.status = visit_in.status
    if visit_in.admin_notes is not None:
        visit.admin_notes = visit_in.admin_notes
    if visit_in.scheduled_at:
        visit.scheduled_at = visit_in.scheduled_at
        
    db.commit()
    db.refresh(visit)
    return visit
