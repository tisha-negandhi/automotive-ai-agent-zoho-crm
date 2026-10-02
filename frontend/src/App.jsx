import React, { useEffect, useMemo, useState } from "react";
import Message from "./components/Message";
import InputBox from "./components/InputBox";
import ScenarioButtons from "./components/ScenarioButtons";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const initialMessage = {
  role: "assistant",
  content:
    "Hello! I am your automotive assistant. I can help with vehicles, test drives, bookings, and service requests.",
};

function createSessionId() {
  if (crypto.randomUUID) {
    return crypto.randomUUID();
  }

  return `session-${Date.now()}`;
}

export default function App() {
  const [sessionId, setSessionId] = useState(createSessionId);
  const [messages, setMessages] = useState([initialMessage]);
  const [stage, setStage] = useState(null);
  const [loading, setLoading] = useState(false);

  const [health, setHealth] = useState({
    status: "checking",
    zoho_configured: false,
    ai_configured: false,
  });

  const crmLabel = useMemo(() => {
    return health.zoho_configured
      ? "Zoho CRM Connected"
      : "Zoho CRM Not Configured";
  }, [health.zoho_configured]);

  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend unavailable");
        }

        return response.json();
      })
      .then((data) => {
        setHealth(data);
      })
      .catch(() => {
        setHealth({
          status: "offline",
          zoho_configured: false,
          ai_configured: false,
        });
      });
  }, []);

  const startNewChat = () => {
    if (loading) {
      return;
    }

    setSessionId(createSessionId());
    setMessages([initialMessage]);
    setStage(null);
  };

  const sendMessage = async (message) => {
    if (!message.trim() || loading) {
      return;
    }

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: message,
      },
    ]);

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message,
        }),
      });

      const payload = await response.json();

      if (!response.ok) {
        throw new Error(
          payload.detail?.message ||
            payload.detail ||
            "Request failed"
        );
      }

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: payload.message,
        },
      ]);

      setStage(payload.stage || null);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: `Sorry, I could not process that request. ${
            error.message || "Something went wrong."
          }`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="header-left">
          <div className="brand-mark">A</div>

          <div>
            <div className="brand">
              Automotive AI Assistant
            </div>

            <div className="subtitle">
              Customer lifecycle support
            </div>
          </div>
        </div>

        <div className="header-right">
          <div className="status-group">
            <div
              className={`status-pill ${
                health.zoho_configured ? "ok" : "warn"
              }`}
            >
              <span className="status-dot" />
              {crmLabel}
            </div>

            <div
              className={`status-pill ${
                health.ai_configured ? "ok" : "warn"
              }`}
            >
              <span className="status-dot" />

              {health.ai_configured
                ? "AI Connected"
                : "AI Not Configured"}
            </div>
          </div>

          <button
            className="new-chat-button"
            onClick={startNewChat}
            disabled={loading}
          >
            <span className="plus-icon">+</span>
            New Chat
          </button>
        </div>
      </header>

      <main className="chat-card">
        <div className="chat-topbar">
          <div>
            <div className="chat-title">
              Customer Support
            </div>

            <div className="chat-description">
              Ask about vehicles, test drives, bookings or service
            </div>
          </div>

          {stage && (
            <div className="stage-badge">
              {stage.replaceAll("_", " ")}
            </div>
          )}
        </div>

        <section className="conversation">
          {messages.map((message, index) => (
            <Message
              key={`${message.role}-${index}`}
              {...message}
            />
          ))}

          {loading && (
            <div className="message-row assistant">
              <div className="avatar">AI</div>

              <div className="message-bubble typing">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
            </div>
          )}
        </section>

        <section className="bottom-panel">
          <ScenarioButtons
            onSelect={sendMessage}
            disabled={loading}
          />

          <InputBox
            onSend={sendMessage}
            disabled={loading}
          />

          <div className="composer-hint">
            Enter to send · Shift + Enter for a new line
          </div>
        </section>
      </main>
    </div>
  );
}
