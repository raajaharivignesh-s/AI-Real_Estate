from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.db.models import Property, User, SiteVisit, SupportRequest, Booking
from app.api.deps import get_current_admin

router = APIRouter()

@router.get("/summary")
def get_analytics_summary(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin)):
    total_properties = db.query(Property).count()
    total_users = db.query(User).filter(User.role == 'customer').count()
    total_visits = db.query(SiteVisit).count()
    total_bookings = db.query(Booking).count()
    
    # Visits by status
    visits_by_status = db.query(SiteVisit.status, func.count(SiteVisit.id)).group_by(SiteVisit.status).all()
    visits_dict = {status.name if hasattr(status, 'name') else status: count for status, count in visits_by_status}
    
    # Support requests
    total_support = db.query(SupportRequest).count()
    
    return {
        "properties": {"total": total_properties},
        "users": {"total_customers": total_users},
        "visits": {
            "total": total_visits,
            "by_status": visits_dict
        },
        "bookings": {"total": total_bookings},
        "support": {
            "total": total_support
        }
    }
