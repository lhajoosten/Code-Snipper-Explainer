import React from "react";
import { TestsOutputProps } from "../types";

export function TestsOutput({ result }: TestsOutputProps) {
  return (
    <div className="output-container">
      <div className="output-header">
        <h3>🧪 Test Generation</h3>
        <div className="output-meta">
          <span className="meta-item">
            <strong>Provider:</strong> {result.provider}
          </span>
          <span className="meta-item">
            <strong>Framework:</strong> {result.test_framework}
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
        {result.test_cases.length > 0 && (
          <div className="test-section">
            <h4>📋 Test Cases Covered</h4>
            <ul className="test-cases-list">
              {result.test_cases.map((testCase, index) => (
                <li key={index}>{testCase}</li>
              ))}
            </ul>
          </div>
        )}

        {result.setup_instructions && (
          <div className="test-section">
            <h4>⚙️ Setup Instructions</h4>
            <div className="setup-content">
              {result.setup_instructions.split("\n").map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          </div>
        )}

        <div className="test-section">
          <h4>💻 Generated Test Code</h4>
          <div className="code-block">
            <pre>
              <code>{result.test_code}</code>
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
