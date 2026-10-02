# Automotive AI Customer Agent Backend

FastAPI backend for the automotive OEM assessment. It contains:

* Zoho OAuth refresh token handling
* Zoho CRM service layer
* Lead creation and lookup
* Deal search and follow up update
* Booking search using a custom Bookings module
* Service Case creation linked to an existing Contact when possible
* In memory conversation state
* Groq tool calling agent
* Vehicle demo catalog
* Test endpoints for CRM integration

## Project structure

```text
backend/
├── app/
│   ├── agent/
│   │   └── tools.py
│   ├── core/
│   │   ├── config.py
│   │   └── state.py
│   ├── data/
│   │   └── vehicles.json
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── crm_service.py
│   │   ├── llm_service.py
│   │   ├── vehicle_service.py
│   │   └── zoho_client.py
│   └── main.py
├── scripts/
│   └── test_zoho.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## Setup

Create a Python virtual environment and install dependencies.

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

macOS or Linux activation:

```bash
source venv/bin/activate
```

Copy `.env.example` to `.env` and add your Zoho credentials.

```bash
copy .env.example .env
```

Do not commit `.env`.

## Required Zoho values

The backend expects:

```text
ZOHO_CLIENT_ID
ZOHO_CLIENT_SECRET
ZOHO_REFRESH_TOKEN
ZOHO_ACCOUNTS_URL=https://accounts.zoho.in
ZOHO_API_DOMAIN=https://www.zohoapis.in
```

It also expects the API names of your custom Zoho fields. These are configurable through `.env` because Zoho can assign different API names to custom fields.

## Verify the backend

From the `backend` directory:

```bash
python scripts/test_zoho.py
```

Then start FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

The interactive API documentation exposes CRM test endpoints and the chat endpoint.

## Chat endpoint

POST `/api/chat`

```json
{
  "session_id": "demo-1",
  "message": "I want to know about the Thar"
}
```

The agent keeps in memory session history for the current backend process. For a production implementation, replace this store with Redis or a persistent database.

## AI setup

The LLM layer uses Groq local tool calling. Set:

```text
GROQ_API_KEY=your_key
GROQ_MODEL=llama-3.3-70b-versatile
```

The application starts without the Groq key so that the Zoho integration can be tested independently. The chat endpoint will tell you when AI is not configured.

## Security notes

* Never put Zoho secrets in React.
* Never commit `.env`.
* The refresh token stays on the backend.
* Access tokens are generated server side from the refresh token.
* The agent is instructed not to invent CRM information.
* Demo vehicle pricing is explicitly labeled as demo data.
