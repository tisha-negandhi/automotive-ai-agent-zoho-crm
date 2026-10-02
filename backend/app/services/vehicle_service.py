import json
from pathlib import Path
from typing import Any


class VehicleService:
    def __init__(self) -> None:
        path = Path(__file__).resolve().parents[1] / "data" / "vehicles.json"
        with path.open("r", encoding="utf-8") as file:
            self.vehicles: dict[str, Any] = json.load(file)

    def get_vehicle_info(self, vehicle_model: str, variant: str | None = None) -> dict[str, Any]:
        normalized = vehicle_model.strip().lower()
        for name, data in self.vehicles.items():
            if name.lower() == normalized:
                result = {"vehicle_model": name, **data}
                if variant:
                    result["requested_variant"] = variant
                return result
        return {
            "vehicle_model": vehicle_model,
            "found": False,
            "message": "Vehicle is not present in the demo catalog.",
        }
