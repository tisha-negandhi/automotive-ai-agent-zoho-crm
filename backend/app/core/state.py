from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class SessionState:
    session_id: str
    stage: str | None = None
    collected: dict[str, Any] = field(default_factory=dict)
    crm_context: dict[str, Any] = field(default_factory=dict)
    messages: list[dict[str, Any]] = field(default_factory=list)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class InMemorySessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, SessionState] = {}

    def get_or_create(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState(session_id=session_id)
        session = self._sessions[session_id]
        session.updated_at = datetime.now(timezone.utc)
        return session

    def update_from_tool(self, session_id: str, tool_name: str, arguments: dict[str, Any], result: dict[str, Any]) -> None:
        session = self.get_or_create(session_id)
        session.collected.update({k: v for k, v in arguments.items() if v not in (None, "")})

        stage_by_tool = {
            "get_vehicle_info": "NEW_LEAD",
            "create_lead": "NEW_LEAD",
            "search_deal": "ONGOING_PIPELINE",
            "update_deal_follow_up": "ONGOING_PIPELINE",
            "search_booking": "BOOKED_VEHICLE",
            "create_service_case": "POST_PURCHASE_SERVICE",
        }
        if tool_name in stage_by_tool:
            session.stage = stage_by_tool[tool_name]

        if isinstance(result, dict):
            data = result.get("data")
            if isinstance(data, list) and data:
                first = data[0]
                if isinstance(first, dict) and first.get("id"):
                    session.crm_context[tool_name] = {"record_id": first.get("id")}
            elif result.get("id"):
                session.crm_context[tool_name] = {"record_id": result.get("id")}

        session.updated_at = datetime.now(timezone.utc)


session_store = InMemorySessionStore()
