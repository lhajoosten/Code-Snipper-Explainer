import React from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import {
  oneDark,
  oneLight,
  darcula,
  materialDark,
} from "react-syntax-highlighter/dist/esm/styles/prism";
import remarkGfm from "remark-gfm";
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
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ node, className, children, ...props }: any) {
                    const match = /language-(\w+)/.exec(className || "");
                    const isInline = !match;
                    return !isInline && match ? (
                      <SyntaxHighlighter
                        style={materialDark}
                        language={match[1]}
                        PreTag="div"
                        showLineNumbers={true}
                        wrapLines={true}
                        wrapLongLines={true}
                        customStyle={{
                          margin: "0.5rem 0",
                          borderRadius: "0.5rem",
                          fontSize: "0.875rem",
                        }}
                        {...props}
                      >
                        {String(children).replace(/\n$/, "")}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                }}
              >
                {result.setup_instructions}
              </ReactMarkdown>
            </div>
          </div>
        )}

        <div className="test-section">
          <h4>💻 Generated Test Code</h4>
          <div className="code-block">
            <SyntaxHighlighter
              style={materialDark}
              language="python"
              PreTag="div"
              showLineNumbers={true}
              wrapLines={true}
              wrapLongLines={true}
              customStyle={{
                margin: 0,
                borderRadius: "0.5rem",
                fontSize: "0.875rem",
                lineHeight: "1.5",
              }}
            >
              {result.test_code}
            </SyntaxHighlighter>
          </div>
        </div>
      </div>
    </div>
  );
}
