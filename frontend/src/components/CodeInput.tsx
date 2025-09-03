import React from "react";

interface CodeInputProps {
  code: string;
  language: string;
  onCodeChange: (code: string) => void;
  onLanguageChange: (language: string) => void;
  onExplain: () => void;
  onReset: () => void;
  disabled?: boolean;
}

const SUPPORTED_LANGUAGES = [
  { value: "", label: "Auto-detect" },
  { value: "javascript", label: "JavaScript" },
  { value: "typescript", label: "TypeScript" },
  { value: "python", label: "Python" },
  { value: "java", label: "Java" },
  { value: "csharp", label: "C#" },
  { value: "cpp", label: "C++" },
  { value: "rust", label: "Rust" },
  { value: "go", label: "Go" },
  { value: "sql", label: "SQL" },
];

export function CodeInput({
  code,
  language,
  onCodeChange,
  onLanguageChange,
  onExplain,
  onReset,
  disabled = false,
}: CodeInputProps) {
  const isCodeEmpty = !code.trim();

  return (
    <div className="code-input">
      <div className="input-header">
        <h2>📝 Code Input</h2>
        <div className="language-selector">
          <label htmlFor="language">Language:</label>
          <select
            id="language"
            value={language}
            onChange={(e) => onLanguageChange(e.target.value)}
            disabled={disabled}
          >
            {SUPPORTED_LANGUAGES.map((lang) => (
              <option key={lang.value} value={lang.value}>
                {lang.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <textarea
        className="code-textarea"
        placeholder="Paste your code here..."
        value={code}
        onChange={(e) => onCodeChange(e.target.value)}
        disabled={disabled}
        rows={20}
      />

      <div className="input-footer">
        <div className="code-stats">
          <span>Lines: {code.split("\n").length}</span>
          <span>Characters: {code.length}</span>
        </div>

        <div className="input-actions">
          <button
            onClick={onReset}
            className="btn btn-secondary"
            disabled={disabled || isCodeEmpty}
          >
            🗑️ Clear
          </button>
          <button
            onClick={onExplain}
            className="btn btn-primary"
            disabled={disabled || isCodeEmpty}
          >
            {disabled ? "⏳ Analyzing..." : "🤖 Explain Code"}
          </button>
        </div>
      </div>
    </div>
  );
}
