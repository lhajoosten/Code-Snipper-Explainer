import React, { useState } from "react";
import { CodeInput } from "./components/CodeInput";
import { ExplanationOutput } from "./components/ExplanationOutput";
import { Header } from "./components/Header";
import { LoadingSpinner } from "./components/LoadingSpinner";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { useExplainCode } from "./hooks/useExplainCode";
import "./App.css";

interface ExplanationResult {
  explanation: string;
  line_count: number;
  character_count: number;
  provider: string;
  placeholder: boolean;
}

export default function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState<string>("");
  const { explainCode, isLoading, error, result, clearError } =
    useExplainCode();

  const handleExplain = async () => {
    if (!code.trim()) return;

    clearError();
    await explainCode({ code: code.trim(), language: language || undefined });
  };

  const handleReset = () => {
    setCode("");
    setLanguage("");
    clearError();
  };

  return (
    <ErrorBoundary>
      <div className="app">
        <Header />

        <main className="main-content">
          <div className="container">
            <div className="grid">
              <div className="input-section">
                <CodeInput
                  code={code}
                  language={language}
                  onCodeChange={setCode}
                  onLanguageChange={setLanguage}
                  onExplain={handleExplain}
                  onReset={handleReset}
                  disabled={isLoading}
                />
              </div>

              <div className="output-section">
                {isLoading && <LoadingSpinner />}
                {error && (
                  <div className="error-container">
                    <h3>❌ Error</h3>
                    <p>{error}</p>
                    <button onClick={clearError} className="btn btn-secondary">
                      Clear Error
                    </button>
                  </div>
                )}
                {result && !isLoading && <ExplanationOutput result={result} />}
              </div>
            </div>
          </div>
        </main>
      </div>
    </ErrorBoundary>
  );
}
