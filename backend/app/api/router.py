from fastapi import APIRouter
from pydantic import BaseModel
from app.api.routes import auth, properties, wishlist, visits, bookings, support, admin_visits, admin_bookings, admin_support, chat, analytics

api_router = APIRouter()

class HealthResponse(BaseModel):
    status: str

@api_router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(wishlist.router, prefix="/wishlist", tags=["wishlist"])

api_router.include_router(visits.router, prefix="/visits", tags=["visits"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(support.router, prefix="/support", tags=["support"])

api_router.include_router(admin_visits.router, prefix="/admin/visits", tags=["admin_visits"])
api_router.include_router(admin_bookings.router, prefix="/admin/bookings", tags=["admin_bookings"])
api_router.include_router(admin_support.router, prefix="/admin/support", tags=["admin_support"])

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(analytics.router, prefix="/admin/analytics", tags=["analytics"])
