from sqlalchemy.orm import Session
from app.db.models import Property, SiteVisit, VisitStatusEnum, SupportRequest, SupportPriorityEnum, User, Booking
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

def search_properties(
    db: Session,
    city: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    property_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Search for properties based on criteria."""
    query = db.query(Property)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    if property_type:
        query = query.filter(Property.property_type == property_type)
        
    results = query.limit(5).all()
    
    return [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "city": p.city,
            "type": p.property_type.name
        }
        for p in results
    ]

def calculate_emi(principal: float, rate: float, years: int) -> float:
    """Calculate Equated Monthly Installment for a loan."""
    if rate == 0:
        return principal / (years * 12)
    r = (rate / 100) / 12
    n = years * 12
    emi = principal * r * ((1 + r)**n) / (((1 + r)**n) - 1)
    return round(emi, 2)

def book_site_visit(db: Session, customer_id: int, property_id: int, scheduled_at: str) -> str:
    """Book a site visit for a property."""
    try:
        dt = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        visit = SiteVisit(
            customer_id=customer_id,
            property_id=property_id,
            scheduled_at=dt,
            status=VisitStatusEnum.requested
        )
        db.add(visit)
        db.commit()
        return f"Site visit successfully requested for Property ID {property_id} at {scheduled_at}."
    except Exception as e:
        return f"Failed to book visit: {str(e)}"

def create_support_ticket(db: Session, customer_id: int, subject: str, description: str, category: str = "General") -> str:
    """Create a support ticket for the customer."""
    try:
        req = SupportRequest(
            customer_id=customer_id,
            subject=subject,
            description=description,
            category=category,
            priority=SupportPriorityEnum.medium
        )
        db.add(req)
        db.commit()
        return f"Support request '{subject}' created successfully."
    except Exception as e:
        return f"Failed to create support request: {str(e)}"

def get_analytics_summary_tool(db: Session) -> str:
    """Get the overall analytics summary of the platform including properties, users, visits, and support requests."""
    total_properties = db.query(Property).count()
    total_users = db.query(User).filter(User.role == 'customer').count()
    total_visits = db.query(SiteVisit).count()
    total_bookings = db.query(Booking).count()
    total_support = db.query(SupportRequest).count()
    
    summary = {
        "total_properties": total_properties,
        "total_customers": total_users,
        "total_site_visits": total_visits,
        "total_bookings": total_bookings,
        "total_support_tickets": total_support
    }
    return json.dumps(summary)
