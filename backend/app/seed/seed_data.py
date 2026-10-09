import logging
from sqlalchemy.orm import Session
import datetime
from app.db.session import engine, SessionLocal
from app.db.models import (
    User, CustomerProfile, Property, LandDetails, PropertyInterest, Wishlist,
    SiteVisit, Booking, SupportRequest, RoleEnum, PropertyTypeEnum, AvailabilityEnum,
    VisitStatusEnum, BookingStatusEnum, SupportPriorityEnum, SupportStatusEnum
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fake simple hash for seeded users ("password123")
FAKE_HASH = "$2b$12$ISnXOCrqhYZbIVF4PJgjgedh3FrbsjuKb9oAifhmBxJhuLXKQQ3nW"

def seed_users(db: Session):
    for i in range(1, 11):
        email = f"customer{i}@demo.com"
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                password_hash=FAKE_HASH,
                full_name=f"Demo Customer {i}",
                role=RoleEnum.customer,
                is_active=True
            )
            db.add(user)
            db.flush()
            
            profile = CustomerProfile(
                user_id=user.id,
                phone=f"555-010{i}",
                preferred_locations=["Coimbatore", "Chennai"],
                budget_min=1000000.0,
                budget_max=50000000.0,
                preferred_type=PropertyTypeEnum.apartment,
                preferred_bedrooms=2
            )
            db.add(profile)
    
    # Add an admin
    admin_email = "admin@demo.com"
    admin = db.query(User).filter(User.email == admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            password_hash=FAKE_HASH,
            full_name="Demo Admin",
            role=RoleEnum.admin,
            is_active=True
        )
        db.add(admin)
        
    db.commit()

def seed_properties(db: Session):
    cities = ["Coimbatore", "Chennai", "Bengaluru"]
    types = [PropertyTypeEnum.apartment, PropertyTypeEnum.villa, PropertyTypeEnum.house, PropertyTypeEnum.land]
    
    images = [
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80",
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80",
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80",
        "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80",
        "https://images.unsplash.com/photo-1600566753086-00f18efc2291?w=800&q=80"
    ]
    adjectives = ["Luxury", "Modern", "Cozy", "Spacious", "Elegant"]
    
    for i in range(1, 51):
        ptype = types[i % len(types)]
        city = cities[i % len(cities)]
        locality = f"Locality {i%5}"
        adj = adjectives[i % len(adjectives)]
        title = f"{adj} {ptype.name.capitalize()} in {locality} ({i})"
        
        prop = db.query(Property).filter(Property.title == title).first()
        if not prop:
            price = 2000000.0 + (i * 500000.0)
            
            prop = Property(
                title=title,
                description=f"A wonderful {adj.lower()} {ptype.name} located in {city}.",
                property_type=ptype,
                price=price,
                city=city,
                locality=locality,
                address=f"{i} Demo Street, {city}",
                area_sqft=1000.0 + (i * 100),
                bedrooms=3 if ptype != PropertyTypeEnum.land else None,
                bathrooms=2 if ptype != PropertyTypeEnum.land else None,
                amenities=["Parking", "Security"] if ptype != PropertyTypeEnum.land else [],
                image_urls=[images[i % len(images)]],
                availability_status=AvailabilityEnum.available
            )
            db.add(prop)
            db.flush()
            
            if ptype == PropertyTypeEnum.land:
                land = LandDetails(
                    property_id=prop.id,
                    plot_area_sqft=prop.area_sqft,
                    road_access="Yes",
                    land_use_type="Residential"
                )
                db.add(land)
    db.commit()

def seed_workflows(db: Session):
    # Visits: 15 visits
    users = db.query(User).filter(User.role == RoleEnum.customer).limit(5).all()
    properties = db.query(Property).all()
    
    if users and properties:
        for i in range(15):
            u = users[i % len(users)]
            p = properties[i % len(properties)]
            visit = db.query(SiteVisit).filter(SiteVisit.customer_id == u.id, SiteVisit.property_id == p.id).first()
            if not visit:
                visit = SiteVisit(
                    customer_id=u.id,
                    property_id=p.id,
                    scheduled_at=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=i+1),
                    status=VisitStatusEnum.requested
                )
                db.add(visit)
                
    # Bookings: 8 bookings
    if len(users) >= 2 and len(properties) >= 8:
        for i in range(8):
            u = users[i % 2]
            p = properties[15 + i] # diff properties
            ref = f"BKG-DEMO-{i+1}"
            bkg = db.query(Booking).filter(Booking.booking_reference == ref).first()
            if not bkg:
                bkg = Booking(
                    customer_id=u.id,
                    property_id=p.id,
                    booking_reference=ref,
                    status=BookingStatusEnum.confirmed,
                    payment_status="Paid"
                )
                db.add(bkg)
                
    # Support: 10 requests
    for i in range(10):
        u = users[i % len(users)]
        subj = f"Demo Support {i+1}"
        req = db.query(SupportRequest).filter(SupportRequest.subject == subj).first()
        if not req:
            req = SupportRequest(
                customer_id=u.id,
                category="General",
                subject=subj,
                description="I have a question about my account.",
                priority=SupportPriorityEnum.low,
                status=SupportStatusEnum.open
            )
            db.add(req)
            
    db.commit()

def run_seed():
    db = SessionLocal()
    try:
        logger.info("Seeding users...")
        seed_users(db)
        logger.info("Seeding properties...")
        seed_properties(db)
        logger.info("Seeding workflows...")
        seed_workflows(db)
        logger.info("Seed complete.")
    except Exception as e:
        db.rollback()
        logger.error(f"Seeding failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
