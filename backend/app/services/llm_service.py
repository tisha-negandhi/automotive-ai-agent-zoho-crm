import json
from typing import Any

from groq import Groq

from app.core.config import settings
from app.agent.tools import AgentTools, tool_schemas
from app.core.state import SessionState, session_store


SYSTEM_PROMPT = """
You are an enterprise automotive OEM customer assistant.

Your job is to help customers across four lifecycle stages:
1. NEW_LEAD: unidentified visitor asking about vehicles, variants, features, demo pricing, or a test drive.
2. ONGOING_PIPELINE: existing prospect checking a test drive, quotation, dealer contact, or follow up preference.
3. BOOKED_VEHICLE: customer checking a booking, delivery timeline, VIN allocation, or balance payment information.
4. POST_PURCHASE_SERVICE: existing owner reporting a complaint, asking about service, or booking maintenance.

Core behavior:
* Use conversation history. Do not treat each message as an independent conversation.
* Do not invent CRM information.
* Do not claim a deal, booking, test drive, VIN, delivery date, payment link, or service case exists unless a tool result supports it.
* After create_service_case succeeds, include the actual Case ID returned by the tool in the final customer response. Never invent or modify a Case ID.
* Ask for only the information needed for the current workflow.
* Never ask for a booking ID and phone number if the customer has already provided one sufficient identifier.
* For a new lead, collect full name, phone, email, preferred city, vehicle model, and variant before create_lead.
* You may answer vehicle catalog questions with get_vehicle_info. Catalog prices in this demo are explicitly demo data, not live market pricing.
* For ongoing pipeline customers, ask for the Deal ID and use search_deal to retrieve the existing Deal. Use the Deal's Stage, Contact, Closing Date, Amount, and Description to answer questions about the customer's test drive or sales progress. Do not invent test drive information that is not present in the Deal.
* For booked vehicles, the booking is represented by a Closed Won Deal in Zoho CRM. Ask for the Deal ID and use search_booking to retrieve the booking information. The Deal Description may contain the Booking ID, vehicle, variant, booking status, allocation stage, VIN, delivery timeline, and balance payment information. Never invent booking information that is not present in the CRM record.
* For service, collect registration number, service or issue type, preferred service center, and issue description. Odometer and preferred date should be collected when available. Use create_service_case only after the required information has been collected.
* After a successful create_service_case result, confirm that the service request was created and include the exact Case ID returned by Zoho CRM. Also summarize the relevant service details. Never invent a Case ID.
* If a CRM lookup returns no record, clearly say the record could not be found and ask for another supported identifier.
* Keep the tone professional, warm, concise, and appropriate for an automotive OEM.
* Do not expose internal tool names, API details, tokens, or implementation details to the customer.
""".strip()


class LLMService:
    def __init__(self, tools: AgentTools | None = None) -> None:
        self.tools = tools or AgentTools()
        if settings.groq_api_key:
            self.client = Groq(api_key=settings.groq_api_key)
        else:
            self.client = None

    def is_configured(self) -> bool:
        return self.client is not None

    def chat(self, session: SessionState, user_message: str) -> str:
        if not self.client:
            return (
                "The backend is running, but the LLM is not configured yet. "
                "Add GROQ_API_KEY to your .env file when we configure the AI step."
            )

        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *session.messages,
            {"role": "user", "content": user_message},
        ]

        registry = self.tools.registry()
        schemas = tool_schemas()

        for _ in range(5):
            response = self.client.chat.completions.create(
                model=settings.groq_model,
                messages=messages,
                tools=schemas,
                tool_choice="auto",
                temperature=0.2,
                max_completion_tokens=800,
            )

            message = response.choices[0].message
            message_dict = message.model_dump(exclude_none=True) if hasattr(message, "model_dump") else dict(message)
            messages.append(message_dict)

            tool_calls = getattr(message, "tool_calls", None) or []
            if not tool_calls:
                content = message.content or "Sorry, I could not generate a response."
                session.messages.append({"role": "user", "content": user_message})
                session.messages.append({"role": "assistant", "content": content})
                return content

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                argument_text = tool_call.function.arguments or "{}"
                arguments: dict[str, Any] = {}
                try:
                    arguments = json.loads(argument_text)
                except json.JSONDecodeError:
                    result: dict[str, Any] = {"error": "Tool arguments were not valid JSON."}
                else:
                    function = registry.get(function_name)
                    if function is None:
                        result = {"error": f"Unknown tool: {function_name}"}
                    else:
                        try:
                            result = function(**arguments)
                        except Exception as exc:
                            result = {
                                "error": str(exc),
                                "tool": function_name,
                            }

                session_store.update_from_tool(
                    session.session_id,
                    function_name,
                    arguments,
                    result,
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )

        raise RuntimeError("The agent reached its maximum tool-calling iterations.")
