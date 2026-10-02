from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=5000)


class ChatResponse(BaseModel):
    session_id: str
    message: str
    stage: str | None = None
    crm_context: dict[str, Any] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    status: str
    zoho_configured: bool
    ai_configured: bool


class LeadCreateRequest(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    vehicle_model: str
    variant: str
    preferred_city: str


class DealSearchRequest(BaseModel):
    phone: str | None = None
    deal_id: str | None = None


class BookingSearchRequest(BaseModel):
    booking_id: str | None = None
    phone: str | None = None


class DealFollowUpRequest(BaseModel):
    deal_id: str
    follow_up_preference: str


class ServiceCaseRequest(BaseModel):
    phone: str | None = None
    registration_number: str
    odometer: int | None = None
    service_type: str
    service_center: str
    issue_description: str
    preferred_date: str | None = None
