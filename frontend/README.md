# Automotive AI Customer Agent Frontend

React and Vite chat interface for the automotive AI assessment.

## Setup

From the `frontend` directory:

```bash
npm install
npm run dev
```

The frontend expects the FastAPI backend at:

```text
http://127.0.0.1:8000
```

To change it, create `frontend/.env`:

```text
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Included UI

* Responsive chat interface
* CRM and AI connection status
* Loading state
* Lifecycle stage indicator
* Four scenario buttons
* Backend session ID per browser session
