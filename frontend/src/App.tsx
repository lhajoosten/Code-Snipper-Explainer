import React, { useState, useCallback } from "react";
import { CodeInput } from "./components/CodeInput";
import { ExplanationOutput } from "./components/ExplanationOutput";
import { Header } from "./components/Header";
import { LoadingSpinner } from "./components/LoadingSpinner";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { useExplainCode } from "./hooks/useExplainCode";
import { AppState } from "./types";
import "./App.css";

export default function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState<string>("");
  const { explainCode, isLoading, error, result, clearError, clearAll } =
    useExplainCode();

  const handleExplain = useCallback(async () => {
    if (!code.trim()) {
      clearError();
      return;
    }

    await explainCode({
      code: code.trim(),
      language: language || undefined,
    });
  }, [code, language, explainCode, clearError]);

  const handleReset = useCallback(() => {
    setCode("");
    setLanguage("");
    clearAll();
  }, [clearAll]);

  // Optimize code change to prevent unnecessary re-renders
  const handleCodeChange = useCallback((newCode: string) => {
    setCode(newCode);
  }, []);

  const handleLanguageChange = useCallback((newLanguage: string) => {
    setLanguage(newLanguage);
  }, []);

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
                  onCodeChange={handleCodeChange}
                  onLanguageChange={handleLanguageChange}
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
