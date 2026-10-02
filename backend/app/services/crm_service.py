from typing import Any

from app.core.config import settings
from app.services.zoho_client import ZohoClient

class ZohoAPIError(Exception):
    """Raised when a Zoho CRM API request fails."""
    pass

class CRMService:
    def __init__(self, zoho: ZohoClient | None = None) -> None:
        self.zoho = zoho or ZohoClient()

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
        record = {
            "First_Name": first_name,
            "Last_Name": last_name,
            "Phone": phone,
            "Email": email,
            settings.lead_vehicle_field: vehicle_model,
            settings.lead_variant_field: variant,
            settings.lead_city_field: preferred_city,
        }
        return self.zoho.create_record("Leads", record)

    def search_lead_by_phone(self, phone: str) -> dict[str, Any]:
        fields = [
            "id",
            "First_Name",
            "Last_Name",
            "Phone",
            "Email",
            settings.lead_vehicle_field,
            settings.lead_variant_field,
            settings.lead_city_field,
        ]
        return self.zoho.search_records(
            "Leads",
            f"(Phone:equals:{self._escape_criteria_value(phone)})",
            fields,
        )

    def search_deal(self, phone: str | None = None, deal_id: str | None = None,) -> dict[str, Any]:

        fields = [
            "id",
            "Deal_Name",
            "Stage",
            "Contact_Name",
            "Amount",
            "Closing_Date",
            "Description",
        ]

        if deal_id:
            return self.zoho.get_record(
                "Deals",
                deal_id,
                fields=fields,
            )

        if not phone:
            raise ValueError("Provide either phone or deal_id.")

        return self.zoho.search_records(
            "Deals",
            f"(Phone:equals:{self._escape_criteria_value(phone)})",
            fields,
        )

    def update_deal_follow_up(self, deal_id: str, follow_up_preference: str) -> dict[str, Any]:
        return self.zoho.update_record(
            "Deals",
            deal_id,
            {settings.deal_follow_up_field: follow_up_preference},
        )

    def search_booking(
    self,
    booking_id: str | None = None,
    phone: str | None = None,
    deal_id: str | None = None,
) -> dict[str, Any]:

        fields = [
            "id",
            "Deal_Name",
            "Stage",
            "Contact_Name",
            "Closing_Date",
            "Description",
        ]

        if deal_id:
            return self.zoho.get_record(
                "Deals",
                deal_id,
                fields=fields,
            )

        if booking_id:
            raise ValueError(
                "Booking information is stored in a Closed Won Deal. Please provide the Deal ID."
            )

        if phone:
            raise ValueError(
                "Booking information is stored in a Closed Won Deal. Please provide the Deal ID."
            )

        raise ValueError("Please provide the Deal ID.")

    def search_contact_by_phone(self, phone: str) -> dict[str, Any]:
        return self.zoho.search_records(
            "Contacts",
            f"(Phone:equals:{self._escape_criteria_value(phone)})",
            ["id", "First_Name", "Last_Name", "Phone", "Email"],
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
        record: dict[str, Any] = {
            "Subject": f"Service Request - {registration_number}",
            "Case_Origin": "Chat",
            "Status": "New",
            settings.case_registration_field: registration_number,
            settings.case_service_type_field: service_type,
            settings.case_service_center_field: service_center,
            settings.case_issue_field: issue_description,
        }

        if odometer is not None:
            record[settings.case_odometer_field] = odometer
        if preferred_date:
            record[settings.case_preferred_date_field] = preferred_date

        if phone and settings.case_contact_field:
            contact_result = self.search_contact_by_phone(phone)
            contacts = contact_result.get("data", [])
            if contacts:
                record[settings.case_contact_field] = {"id": contacts[0]["id"]}

        result = self.zoho.create_record("Cases", record)
        print("ZOHO CASE CREATION RESPONSE:", result)
        return result

    @staticmethod
    def _escape_criteria_value(value: str) -> str:
        return value.replace("\\", "\\\\").replace("'", "\\'")

    def test_connection(self) -> dict[str, Any]:
        return self.zoho.get(
            "users",
            params={
                "type": "CurrentUser",
            },
        )
