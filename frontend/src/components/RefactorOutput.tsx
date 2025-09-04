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
              {result.explanation}
            </ReactMarkdown>
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
              {result.refactored_code}
            </SyntaxHighlighter>
          </div>
        </div>
      </div>
    </div>
  );
}
