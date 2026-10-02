from typing import Any

import requests

from app.core.config import settings


class ZohoAPIError(RuntimeError):
    def __init__(self, status_code: int, payload: Any) -> None:
        self.status_code = status_code
        self.payload = payload
        super().__init__(f"Zoho API error {status_code}: {payload}")


class ZohoClient:
    def __init__(self) -> None:
        self.accounts_url = settings.zoho_accounts_url.rstrip("/")
        self.api_domain = settings.zoho_api_domain.rstrip("/")

    def _require_credentials(self) -> None:
        missing = []
        for name, value in {
            "ZOHO_CLIENT_ID": settings.zoho_client_id,
            "ZOHO_CLIENT_SECRET": settings.zoho_client_secret,
            "ZOHO_REFRESH_TOKEN": settings.zoho_refresh_token,
        }.items():
            if not value:
                missing.append(name)
        if missing:
            raise RuntimeError(f"Missing Zoho environment variables: {', '.join(missing)}")

    def get_access_token(self) -> str:
        self._require_credentials()
        response = requests.post(
            f"{self.accounts_url}/oauth/v2/token",
            params={
                "refresh_token": settings.zoho_refresh_token,
                "client_id": settings.zoho_client_id,
                "client_secret": settings.zoho_client_secret,
                "grant_type": "refresh_token",
            },
            timeout=30,
        )
        payload = self._parse_response(response)
        token = payload.get("access_token")
        if not token:
            raise RuntimeError(f"Zoho token response did not contain access_token: {payload}")
        if payload.get("api_domain"):
            self.api_domain = str(payload["api_domain"]).rstrip("/")
        return token

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Zoho-oauthtoken {self.get_access_token()}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _parse_response(response: requests.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError:
            payload = {"raw": response.text}
        if not response.ok:
            raise ZohoAPIError(response.status_code, payload)
        return payload

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.api_domain}/crm/v8/{path.lstrip('/')}"
        response = requests.get(url, headers=self._headers(), params=params, timeout=30)
        return self._parse_response(response)

    def post(self, path: str, body: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.api_domain}/crm/v8/{path.lstrip('/')}"
        response = requests.post(url, headers=self._headers(), params=params, json=body, timeout=30)
        return self._parse_response(response)

    def put(self, path: str, body: dict[str, Any], params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.api_domain}/crm/v8/{path.lstrip('/')}"
        response = requests.put(url, headers=self._headers(), params=params, json=body, timeout=30)
        return self._parse_response(response)

    def get_module_records(self, module_api_name: str, fields: list[str], per_page: int = 10) -> dict[str, Any]:
        return self.get(module_api_name, params={"fields": ",".join(fields), "per_page": per_page})

    def search_records(self, module_api_name: str, criteria: str, fields: list[str] | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"criteria": criteria}
        if fields:
            params["fields"] = ",".join(fields)
        return self.get(f"{module_api_name}/search", params=params)

    def get_record(self, module_api_name: str, record_id: str, fields: list[str] | None = None) -> dict[str, Any]:
        params = {"fields": ",".join(fields)} if fields else None
        return self.get(f"{module_api_name}/{record_id}", params=params)

    def create_record(self, module_api_name: str, record: dict[str, Any]) -> dict[str, Any]:
        return self.post(module_api_name, {"data": [record]})

    def update_record(self, module_api_name: str, record_id: str, record: dict[str, Any]) -> dict[str, Any]:
        return self.put(f"{module_api_name}/{record_id}", {"data": [record]})
