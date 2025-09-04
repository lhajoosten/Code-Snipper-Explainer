import React from "react";
import { RefactorOutputProps } from "../types";

export function RefactorOutput({ result }: RefactorOutputProps) {
  return (
    <div className="output-container">
      <div className="output-header">
        <h3>🔧 Code Refactoring</h3>
        <div className="output-meta">
          <span className="meta-item">
            <strong>Provider:</strong> {result.provider}
          </span>
          <span className="meta-item">
            <strong>Lines:</strong> {result.line_count}
          </span>
          <span className="meta-item">
            <strong>Characters:</strong> {result.character_count}
          </span>
        </div>
      </div>

      <div className="output-content">
        <div className="refactor-section">
          <h4>📋 Refactoring Analysis</h4>
          <div className="explanation-content">
            {result.explanation.split("\n").map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </div>

        {result.improvements.length > 0 && (
          <div className="refactor-section">
            <h4>✨ Key Improvements</h4>
            <ul className="improvements-list">
              {result.improvements.map((improvement, index) => (
                <li key={index}>{improvement}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="refactor-section">
          <h4>💻 Refactored Code</h4>
          <div className="code-block">
            <pre>
              <code>{result.refactored_code}</code>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
