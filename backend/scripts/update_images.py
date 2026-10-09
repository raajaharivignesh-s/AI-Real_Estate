from app.db.session import SessionLocal
from app.db.models import Property
import random

images = [
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80",
    "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80",
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80",
    "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80",
    "https://images.unsplash.com/photo-1600566753086-00f18efc2291?w=800&q=80",
    "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&q=80",
    "https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=800&q=80"
]

adjectives = ["Luxury", "Modern", "Cozy", "Spacious", "Elegant", "Beautiful"]

db = SessionLocal()
properties = db.query(Property).all()

for prop in properties:
    prop.image_urls = [random.choice(images)]
    adj = random.choice(adjectives)
    prop.title = f"{adj} {prop.property_type.name.capitalize()} in {prop.locality}"
    prop.description = f"Experience premium living with this {adj.lower()} {prop.property_type.name} located in the heart of {prop.city}. Perfect for families and professionals alike."

db.commit()
db.close()
print("Updated properties with images and descriptions!")
