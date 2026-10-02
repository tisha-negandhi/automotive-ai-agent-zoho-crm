import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    zoho_client_id: str = os.getenv("ZOHO_CLIENT_ID", "")
    zoho_client_secret: str = os.getenv("ZOHO_CLIENT_SECRET", "")
    zoho_refresh_token: str = os.getenv("ZOHO_REFRESH_TOKEN", "")
    zoho_accounts_url: str = os.getenv("ZOHO_ACCOUNTS_URL", "https://accounts.zoho.in")
    zoho_api_domain: str = os.getenv("ZOHO_API_DOMAIN", "https://www.zohoapis.in")
    zoho_bookings_module_api_name: str = os.getenv("ZOHO_BOOKINGS_MODULE_API_NAME", "Bookings")

    lead_vehicle_field: str = os.getenv("ZOHO_LEAD_VEHICLE_FIELD", "Vehicle_Model")
    lead_variant_field: str = os.getenv("ZOHO_LEAD_VARIANT_FIELD", "Interested_Variant")
    lead_city_field: str = os.getenv("ZOHO_LEAD_CITY_FIELD", "Preferred_City")

    deal_customer_phone_field: str = os.getenv("ZOHO_DEAL_CUSTOMER_PHONE_FIELD", "Customer_Phone")
    deal_vehicle_field: str = os.getenv("ZOHO_DEAL_VEHICLE_FIELD", "Vehicle_Model")
    deal_test_drive_date_field: str = os.getenv("ZOHO_DEAL_TEST_DRIVE_DATE_FIELD", "Test_Drive_Date")
    deal_test_drive_time_field: str = os.getenv("ZOHO_DEAL_TEST_DRIVE_TIME_FIELD", "Test_Drive_Time")
    deal_dealer_field: str = os.getenv("ZOHO_DEAL_DEALER_FIELD", "Dealer_Name")
    deal_follow_up_field: str = os.getenv("ZOHO_DEAL_FOLLOW_UP_FIELD", "Follow_Up_Preference")

    booking_id_field: str = os.getenv("ZOHO_BOOKING_ID_FIELD", "Booking_ID")
    booking_vehicle_field: str = os.getenv("ZOHO_BOOKING_VEHICLE_FIELD", "Vehicle_Model")
    booking_status_field: str = os.getenv("ZOHO_BOOKING_STATUS_FIELD", "Booking_Status")
    booking_allocation_stage_field: str = os.getenv("ZOHO_BOOKING_ALLOCATION_STAGE_FIELD", "Allocation_Stage")
    booking_vin_field: str = os.getenv("ZOHO_BOOKING_VIN_FIELD", "VIN")
    booking_delivery_date_field: str = os.getenv("ZOHO_BOOKING_DELIVERY_DATE_FIELD", "Expected_Delivery_Date")
    booking_payment_link_field: str = os.getenv("ZOHO_BOOKING_PAYMENT_LINK_FIELD", "Balance_Payment_Link")
    booking_phone_field: str = os.getenv("ZOHO_BOOKING_PHONE_FIELD", "Phone")

    case_registration_field: str = os.getenv("ZOHO_CASE_REGISTRATION_FIELD", "Registration_Number")
    case_odometer_field: str = os.getenv("ZOHO_CASE_ODOMETER_FIELD", "Odometer")
    case_service_type_field: str = os.getenv("ZOHO_CASE_SERVICE_TYPE_FIELD", "Service_Type")
    case_service_center_field: str = os.getenv("ZOHO_CASE_SERVICE_CENTER_FIELD", "Preferred_Service_Center")
    case_issue_field: str = os.getenv("ZOHO_CASE_ISSUE_FIELD", "Issue_Description")
    case_preferred_date_field: str = os.getenv("ZOHO_CASE_PREFERRED_DATE_FIELD", "Preferred_Date")
    case_contact_field: str = os.getenv("ZOHO_CASE_CONTACT_FIELD", "Contact_Name")

    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
