from typing import Any, Callable

from app.services.crm_service import CRMService
from app.services.vehicle_service import VehicleService


class AgentTools:
    def __init__(self, crm: CRMService | None = None, vehicle_service: VehicleService | None = None) -> None:
        self.crm = crm or CRMService()
        self.vehicle_service = vehicle_service or VehicleService()

    def get_vehicle_info(self, vehicle_model: str, variant: str | None = None) -> dict[str, Any]:
        return self.vehicle_service.get_vehicle_info(vehicle_model, variant)

    def create_lead(
        self,
        first_name: str,
        last_name: str,
        phone: str,
        email: str,
        vehicle_model: str,
        variant: str,
        preferred_city: str,
    ) -> dict[str, Any]:
        return self.crm.create_lead(
            first_name,
            last_name,
            phone,
            email,
            vehicle_model,
            variant,
            preferred_city,
        )

    def search_deal(self, phone: str | None = None, deal_id: str | None = None) -> dict[str, Any]:
        return self.crm.search_deal(phone=phone, deal_id=deal_id)

    def update_deal_follow_up(self, deal_id: str, follow_up_preference: str) -> dict[str, Any]:
        return self.crm.update_deal_follow_up(deal_id, follow_up_preference)

    def search_booking(
    self,
    booking_id: str | None = None,
    phone: str | None = None,
    deal_id: str | None = None,
) -> dict[str, Any]:
        return self.crm.search_booking(
            booking_id=booking_id,
            phone=phone,
            deal_id=deal_id,
        )

    def create_service_case(
        self,
        phone: str | None,
        registration_number: str,
        odometer: int | None,
        service_type: str,
        service_center: str,
        issue_description: str,
        preferred_date: str | None,
    ) -> dict[str, Any]:
        return self.crm.create_service_case(
            phone=phone,
            registration_number=registration_number,
            odometer=odometer,
            service_type=service_type,
            service_center=service_center,
            issue_description=issue_description,
            preferred_date=preferred_date,
        )

    def registry(self) -> dict[str, Callable[..., dict[str, Any]]]:
        return {
            "get_vehicle_info": self.get_vehicle_info,
            "create_lead": self.create_lead,
            "search_deal": self.search_deal,
            "update_deal_follow_up": self.update_deal_follow_up,
            "search_booking": self.search_booking,
            "create_service_case": self.create_service_case,
        }


def tool_schemas() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "get_vehicle_info",
                "description": "Get demo automotive catalog information such as variants and demo price for a vehicle.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "vehicle_model": {"type": "string"},
                        "variant": {"type": "string"},
                    },
                    "required": ["vehicle_model"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_lead",
                "description": "Create a new CRM lead after all required new lead details have been collected.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "phone": {"type": "string"},
                        "email": {"type": "string"},
                        "vehicle_model": {"type": "string"},
                        "variant": {"type": "string"},
                        "preferred_city": {"type": "string"},
                    },
                    "required": ["first_name", "last_name", "phone", "email", "vehicle_model", "variant", "preferred_city"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_deal",
                "description": "Find an existing CRM Deal using the Deal ID. The Deal contains the customer's ongoing sales and test drive information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "phone": {"type": "string"},
                        "deal_id": {"type": "string"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_deal_follow_up",
                "description": "Update the follow up preference on a known deal.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "deal_id": {"type": "string"},
                        "follow_up_preference": {"type": "string", "enum": ["Phone", "Email", "WhatsApp"]},
                    },
                    "required": ["deal_id", "follow_up_preference"],
                },
            },
        },
        {
    "type": "function",
    "function": {
        "name": "search_booking",
        "description": "Find a booked vehicle using the Deal ID of the Closed Won Deal.",
        "parameters": {
            "type": "object",
            "properties": {
                "deal_id": {
                    "type": "string",
                    "description": "The Zoho Deal ID for the booked vehicle."
                }
            },
            "required": ["deal_id"],
        },
    },
},
        {
            "type": "function",
            "function": {
                "name": "create_service_case",
                "description": "Create a CRM service Case after collecting registration number, issue or service type, odometer if available, preferred service center, and preferred date if available.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "phone": {"type": "string"},
                        "registration_number": {"type": "string"},
                        "odometer": {"type": "integer"},
                        "service_type": {"type": "string"},
                        "service_center": {"type": "string"},
                        "issue_description": {"type": "string"},
                        "preferred_date": {"type": "string"},
                    },
                    "required": ["registration_number", "service_type", "service_center", "issue_description"],
                },
            },
        },
    ]
