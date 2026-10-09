from app.db.session import SessionLocal
from app.db.models import User

valid_hash = "$2b$12$ISnXOCrqhYZbIVF4PJgjgedh3FrbsjuKb9oAifhmBxJhuLXKQQ3nW"

db = SessionLocal()
users = db.query(User).all()
for u in users:
    u.password_hash = valid_hash
db.commit()
db.close()
print("Passwords fixed")
