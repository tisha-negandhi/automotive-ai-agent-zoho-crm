import React, { useState } from "react";

export default function InputBox({ onSend, disabled }) {
  const [value, setValue] = useState("");

  const submit = async () => {
    const message = value.trim();

    if (!message || disabled) {
      return;
    }

    setValue("");
    await onSend(message);
  };

  const handleKeyDown = async (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      await submit();
    }
  };

  return (
    <form
      className="input-area"
      onSubmit={(event) => {
        event.preventDefault();
        submit();
      }}
    >
      <textarea
        value={value}
        onChange={(event) => setValue(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your message..."
        disabled={disabled}
        rows={3}
      />

      <button
        type="submit"
        disabled={disabled || !value.trim()}
      >
        Send
      </button>
    </form>
  );
}
