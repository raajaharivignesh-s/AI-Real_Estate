import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, UniqueConstraint, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .base import Base

class RoleEnum(str, enum.Enum):
    customer = "customer"
    admin = "admin"

class PropertyTypeEnum(str, enum.Enum):
    apartment = "apartment"
    villa = "villa"
    house = "independent_house"
    land = "land"

class AvailabilityEnum(str, enum.Enum):
    available = "available"
    sold = "sold"
    unavailable = "unavailable"

class LegalVerificationEnum(str, enum.Enum):
    verified = "verified"
    not_verified = "not_verified"
    pending = "pending"

class VisitStatusEnum(str, enum.Enum):
    requested = "requested"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    rescheduling_requested = "rescheduling_requested"

class BookingStatusEnum(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class SupportPriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class SupportStatusEnum(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    waiting_for_customer = "waiting_for_customer"
    resolved = "resolved"
    closed = "closed"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), default=RoleEnum.customer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    profile = relationship("CustomerProfile", back_populates="user", uselist=False)

class CustomerProfile(Base):
    __tablename__ = "customer_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    phone = Column(String, nullable=True)
    preferred_locations = Column(JSON, nullable=True)
    budget_min = Column(Float, nullable=True)
    budget_max = Column(Float, nullable=True)
    preferred_type = Column(SQLEnum(PropertyTypeEnum), nullable=True)
    preferred_bedrooms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="profile")

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    property_type = Column(SQLEnum(PropertyTypeEnum), nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    locality = Column(String, nullable=False)
    address = Column(String, nullable=False)
    area_sqft = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    amenities = Column(JSON, nullable=True)
    image_urls = Column(JSON, nullable=True)
    availability_status = Column(SQLEnum(AvailabilityEnum), default=AvailabilityEnum.available, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    land_details = relationship("LandDetails", back_populates="property", uselist=False)

class LandDetails(Base):
    __tablename__ = "land_details"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), unique=True, nullable=False)
    plot_area_sqft = Column(Float, nullable=False)
    plot_length_ft = Column(Float, nullable=True)
    plot_width_ft = Column(Float, nullable=True)
    road_access = Column(String, nullable=True)
    land_use_type = Column(String, nullable=True)
    survey_reference = Column(String, nullable=True)
    legal_verification_status = Column(SQLEnum(LegalVerificationEnum), default=LegalVerificationEnum.not_verified)
    additional_notes = Column(Text, nullable=True)

    property = relationship("Property", back_populates="land_details")

class PropertyInterest(Base):
    __tablename__ = "property_interests"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    status = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('customer_id', 'property_id', name='uix_customer_property_wishlist'),)

class SiteVisit(Base):
    __tablename__ = "site_visits"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(SQLEnum(VisitStatusEnum), default=VisitStatusEnum.requested)
    customer_notes = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    booking_reference = Column(String, unique=True, index=True, nullable=False)
    status = Column(SQLEnum(BookingStatusEnum), default=BookingStatusEnum.pending)
    payment_status = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SupportRequest(Base):
    __tablename__ = "support_requests"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)
    visit_id = Column(Integer, ForeignKey("site_visits.id"), nullable=True)
    category = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(SQLEnum(SupportPriorityEnum), default=SupportPriorityEnum.medium)
    status = Column(SQLEnum(SupportStatusEnum), default=SupportStatusEnum.open)
    resolution_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False) # user, assistant, tool
    content = Column(Text, nullable=False)
    agent_name = Column(String, nullable=True)
    structured_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AgentRun(Base):
    __tablename__ = "agent_runs"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    agent_name = Column(String, nullable=True)
    intent = Column(String, nullable=True)
    status = Column(String, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    tool_summary = Column(Text, nullable=True)
    error_code = Column(String, nullable=True)
