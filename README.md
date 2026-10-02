# Automotive AI Customer Agent

End to end starter project for the Automotive OEM AI Solutions Engineer assessment.

```text
React frontend
      |
      v
FastAPI backend
      |
      +---- in memory session state
      |
      +---- Groq LLM tool calling
      |
      +---- CRM service layer
                  |
                  v
              Zoho CRM
```

## Folders

```text
backend/
frontend/
```

The backend is deliberately implemented without LangChain so the tool orchestration remains explicit and easy to explain during the assessment.

## Current status

The code already contains:

* Zoho refresh token authentication
* CRM API wrapper
* Lead creation
* Lead lookup
* Deal search
* Deal follow up update
* Booking search
* Service Case creation
* Contact lookup for Case linking
* Vehicle demo catalog
* Conversation state
* Groq tool calling loop
* React chat UI
* CRM and AI health indicators

The remaining setup is configuration: enter the Zoho credentials and your actual custom field API names, then add the Groq key when we configure the AI stage.
