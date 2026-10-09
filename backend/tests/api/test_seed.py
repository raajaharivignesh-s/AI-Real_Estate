import pytest
from app.seed.seed_data import run_seed
from app.db.session import SessionLocal
from app.db.models import User, Property, SiteVisit, Booking, SupportRequest

def test_seed_idempotency():
    # Run seed the first time
    run_seed()
    
    db = SessionLocal()
    user_count_1 = db.query(User).count()
    prop_count_1 = db.query(Property).count()
    visit_count_1 = db.query(SiteVisit).count()
    bkg_count_1 = db.query(Booking).count()
    db.close()
    
    # Run seed the second time
    run_seed()
    
    db = SessionLocal()
    user_count_2 = db.query(User).count()
    prop_count_2 = db.query(Property).count()
    visit_count_2 = db.query(SiteVisit).count()
    bkg_count_2 = db.query(Booking).count()
    db.close()
    
    assert user_count_1 == user_count_2
    assert prop_count_1 == prop_count_2
    assert visit_count_1 == visit_count_2
    assert bkg_count_1 == bkg_count_2
    
    assert user_count_1 >= 11  # 10 customers + 1 admin
    assert prop_count_1 >= 50
    assert visit_count_1 >= 15
    assert bkg_count_1 >= 8
