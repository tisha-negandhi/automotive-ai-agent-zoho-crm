import React from "react";
import ReactMarkdown from "react-markdown";

export default function Message({ role, content }) {
  const isAssistant = role === "assistant";

  return (
    <div className={`message-row ${isAssistant ? "assistant" : "user"}`}>
      {isAssistant && <div className="avatar">AI</div>}

      <div className="message-bubble">
        {isAssistant ? (
          <ReactMarkdown>{content}</ReactMarkdown>
        ) : (
          content
        )}
      </div>
    </div>
  );
}