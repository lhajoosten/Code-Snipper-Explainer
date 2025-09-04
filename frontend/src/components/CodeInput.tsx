import React, { memo } from "react";
import { CodeInputProps, SupportedLanguage } from "../types";

const SUPPORTED_LANGUAGES: SupportedLanguage[] = [
  { value: "", label: "Auto-detect" },
  { value: "javascript", label: "JavaScript", extension: "js" },
  { value: "typescript", label: "TypeScript", extension: "ts" },
  { value: "python", label: "Python", extension: "py" },
  { value: "java", label: "Java", extension: "java" },
  { value: "csharp", label: "C#", extension: "cs" },
  { value: "cpp", label: "C++", extension: "cpp" },
  { value: "rust", label: "Rust", extension: "rs" },
  { value: "go", label: "Go", extension: "go" },
  { value: "sql", label: "SQL", extension: "sql" },
];

export const CodeInput = memo<CodeInputProps>(function CodeInput({
  code,
  language,
  onCodeChange,
  onLanguageChange,
  onExplain,
  onRefactor,
  onGenerateTests,
  onReset,
  disabled = false,
}) {
  const isCodeEmpty = !code.trim();
  const characterCount = code.length;
  const lineCount = code ? code.split("\n").length : 0;

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
          <span>Lines: {lineCount}</span>
          <span>Characters: {characterCount}</span>
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
          <button
            onClick={onRefactor}
            className="btn btn-success"
            disabled={disabled || isCodeEmpty}
          >
            {disabled ? "⏳ Refactoring..." : "🔧 Refactor Code"}
          </button>
          <button
            onClick={onGenerateTests}
            className="btn btn-info"
            disabled={disabled || isCodeEmpty}
          >
            {disabled ? "⏳ Generating..." : "🧪 Generate Tests"}
          </button>
        </div>
      </div>
    </div>
  );
});
