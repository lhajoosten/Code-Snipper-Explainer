import React from "react";

interface LoadingSpinnerProps {
  message?: string;
  size?: "small" | "medium" | "large";
}

export function LoadingSpinner({
  message = "Analyzing your code...",
  size = "medium",
}: LoadingSpinnerProps) {
  return (
    <div className="loading-spinner-container">
      <div className={`loading-spinner ${size}`}>
        <div className="spinner-ring">
          <div></div>
          <div></div>
          <div></div>
          <div></div>
        </div>
      </div>

      <div className="loading-content">
        <h3 className="loading-title">🧠 Processing...</h3>
        <p className="loading-message">{message}</p>

        <div className="loading-steps">
          <div className="step active">
            <span className="step-icon">📝</span>
            <span className="step-text">Parsing code</span>
          </div>
          <div className="step active">
            <span className="step-icon">🤖</span>
            <span className="step-text">AI analysis</span>
          </div>
          <div className="step">
            <span className="step-icon">✨</span>
            <span className="step-text">Generating explanation</span>
          </div>
        </div>
      </div>
    </div>
  );
}
