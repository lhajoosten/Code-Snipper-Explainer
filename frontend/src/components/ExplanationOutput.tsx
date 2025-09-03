import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import remarkGfm from "remark-gfm";

interface ExplanationResult {
  explanation: string;
  line_count: number;
  character_count: number;
  provider: string;
  placeholder: boolean;
}

interface ExplanationOutputProps {
  result: ExplanationResult;
}

export function ExplanationOutput({ result }: ExplanationOutputProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(result.explanation);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="explanation-output">
      <div className="output-header">
        <h2>🤖 Code Explanation</h2>
        <div className="output-meta">
          <span
            className={`provider-badge ${
              result.placeholder ? "placeholder" : "real"
            }`}
          >
            {result.provider} {result.placeholder ? "(Demo)" : ""}
          </span>
          <button
            onClick={handleCopy}
            className="btn btn-sm btn-secondary"
            title="Copy explanation"
          >
            {copied ? "✅ Copied!" : "📋 Copy"}
          </button>
        </div>
      </div>

      <div className="explanation-content">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code({ node, inline, className, children, style, ...props }) {
              const match = /language-(\w+)/.exec(className || "");
              const language = match ? match[1] : "";

              if (!inline && language) {
                return (
                  <SyntaxHighlighter
                    style={vscDarkPlus}
                    language={language}
                    PreTag="div"
                    customStyle={{
                      margin: "1rem 0",
                      borderRadius: "0.75rem",
                      fontSize: "0.875rem",
                      lineHeight: "1.5",
                    }}
                    {...props}
                  >
                    {String(children).replace(/\n$/, "")}
                  </SyntaxHighlighter>
                );
              }

              // Handle inline code
              return (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
            // Enhanced handling for other markdown elements
            h1: ({ children }) => (
              <h1
                style={{
                  borderBottom: "2px solid var(--primary-200)",
                  paddingBottom: "0.5rem",
                  marginTop: "2rem",
                  marginBottom: "1rem",
                }}
              >
                {children}
              </h1>
            ),
            h2: ({ children }) => (
              <h2
                style={{
                  marginTop: "1.5rem",
                  marginBottom: "0.75rem",
                  color: "var(--gray-800)",
                }}
              >
                {children}
              </h2>
            ),
            h3: ({ children }) => (
              <h3
                style={{
                  marginTop: "1.25rem",
                  marginBottom: "0.5rem",
                  color: "var(--gray-800)",
                }}
              >
                {children}
              </h3>
            ),
            p: ({ children }) => (
              <p
                style={{
                  marginBottom: "1rem",
                  lineHeight: "1.7",
                }}
              >
                {children}
              </p>
            ),
            ul: ({ children }) => (
              <ul
                style={{
                  marginLeft: "1.5rem",
                  marginBottom: "1rem",
                }}
              >
                {children}
              </ul>
            ),
            ol: ({ children }) => (
              <ol
                style={{
                  marginLeft: "1.5rem",
                  marginBottom: "1rem",
                }}
              >
                {children}
              </ol>
            ),
            li: ({ children }) => (
              <li style={{ marginBottom: "0.25rem" }}>{children}</li>
            ),
            blockquote: ({ children }) => (
              <blockquote
                style={{
                  borderLeft: "4px solid var(--primary-500)",
                  background: "var(--primary-50)",
                  padding: "1rem",
                  margin: "1.5rem 0",
                  borderRadius: "0 0.5rem 0.5rem 0",
                }}
              >
                {children}
              </blockquote>
            ),
            strong: ({ children }) => (
              <strong
                style={{
                  color: "var(--gray-900)",
                  fontWeight: "600",
                }}
              >
                {children}
              </strong>
            ),
          }}
        >
          {result.explanation}
        </ReactMarkdown>
      </div>

      <div className="output-footer">
        <div className="analysis-stats">
          <span>📊 Analyzed {result.line_count} lines</span>
          <span>📏 {result.character_count} characters</span>
        </div>
      </div>
    </div>
  );
}
