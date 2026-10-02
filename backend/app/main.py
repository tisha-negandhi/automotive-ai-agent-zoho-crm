import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.agent.tools import AgentTools
from app.core.config import settings
from app.core.state import session_store
from app.models.schemas import (
    BookingSearchRequest,
    ChatRequest,
    ChatResponse,
    DealFollowUpRequest,
    DealSearchRequest,
    HealthResponse,
    LeadCreateRequest,
    ServiceCaseRequest,
)
from app.services.crm_service import CRMService, ZohoAPIError
from app.services.llm_service import LLMService

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Automotive AI Customer Agent",
    version="1.0.0",
    description="Multistage automotive customer assistant with Zoho CRM integration.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crm = CRMService()
llm = LLMService(AgentTools(crm=crm))


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    zoho_configured = all(
        [
            settings.zoho_client_id,
            settings.zoho_client_secret,
            settings.zoho_refresh_token,
        ]
    )
    return HealthResponse(
        status="ok",
        zoho_configured=zoho_configured,
        ai_configured=llm.is_configured(),
    )


@app.get("/api/crm/test")
def crm_test() -> dict:
    try:
        return crm.test_connection()
    except ZohoAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.payload) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/crm/leads")
def get_leads() -> dict:
    try:
        return crm.zoho.get_module_records(
            "Leads",
            ["id", "First_Name", "Last_Name", "Phone", "Email"],
            per_page=10,
        )
    except ZohoAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.payload) from exc


@app.post("/api/crm/leads")
def create_lead(request: LeadCreateRequest) -> dict:
    try:
        return crm.create_lead(**request.model_dump())
    except ZohoAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.payload) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/crm/deals/search")
def search_deal(request: DealSearchRequest) -> dict:
    if not request.phone and not request.deal_id:
        raise HTTPException(status_code=400, detail="Provide phone or deal_id.")
    try:
        return crm.search_deal(phone=request.phone, deal_id=request.deal_id)
    except ZohoAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.payload) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.patch("/api/crm/deals/{deal_id}/follow-up")
def update_deal_follow_up(deal_id: str, request: DealFollowUpRequest) -> dict:
    try:
        return crm.update_deal_follow_up(deal_id, request.follow_up_preference)
    except ZohoAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.payload) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/crm/bookings/search")
def search_booking(request: BookingSearchRequest) -> dict:
    if not request.booking_id and not request.phone:
        raise HTTPException(status_code=400, detail="Provide booking_id or phone.")
    try:
        return crm.search_booking(booking_id=request.booking_id, phone=request.phone)
    except ZohoAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.payload) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/crm/cases")
def create_service_case(request: ServiceCaseRequest) -> dict:
    try:
        return crm.create_service_case(**request.model_dump())
    except ZohoAPIError as exc:
        raise HTTPException(status_code=502, detail=exc.payload) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    session = session_store.get_or_create(request.session_id)
    try:
        response = llm.chat(session, request.message)
    except ZohoAPIError as exc:
        logger.exception("Zoho API error during chat")
        raise HTTPException(status_code=502, detail=exc.payload) from exc
    except Exception as exc:
        logger.exception("Chat error")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return ChatResponse(
        session_id=request.session_id,
        message=response,
        stage=session.stage,
        crm_context=session.crm_context,
    )
