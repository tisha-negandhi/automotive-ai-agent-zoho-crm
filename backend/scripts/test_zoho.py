from app.services.crm_service import CRMService


crm = CRMService()

print("Testing Zoho connection...")
print(crm.test_connection())

print("\nTesting Leads read...")
print(
    crm.zoho.get_module_records(
        "Leads",
        ["id", "First_Name", "Last_Name", "Phone", "Email"],
        per_page=10,
    )
)
