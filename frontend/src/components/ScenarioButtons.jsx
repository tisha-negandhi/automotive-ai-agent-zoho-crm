import React from "react";
const scenarios = [
  {
    label: "New vehicle",
    message: "I am interested in the Thar.",
  },
  {
    label: "Check test drive",
    message: "I want to check my XUV700 test drive.",
  },
  {
    label: "Track booking",
    message: "I want to check my vehicle booking.",
  },
  {
    label: "Book service",
    message: "I need service for my vehicle.",
  },
];

export default function ScenarioButtons({ onSelect, disabled }) {
  return (
    <div className="scenario-section">
      <div className="scenario-title">Try a scenario</div>
      <div className="scenario-buttons">
        {scenarios.map((scenario) => (
          <button
            key={scenario.label}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(scenario.message)}
          >
            {scenario.label}
          </button>
        ))}
      </div>
    </div>
  );
}
