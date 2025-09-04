import React, { useState, useCallback } from "react";
import { CodeInput } from "./components/CodeInput";
import { ExplanationOutput } from "./components/ExplanationOutput";
import { RefactorOutput } from "./components/RefactorOutput";
import { TestsOutput } from "./components/TestsOutput";
import { Header } from "./components/Header";
import { LoadingSpinner } from "./components/LoadingSpinner";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { useExplainCode } from "./hooks/useExplainCode";
import { useRefactorCode } from "./hooks/useRefactorCode";
import { useGenerateTests } from "./hooks/useGenerateTests";
import { AppState } from "./types";
import "./App.css";

export default function App() {
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState<string>("");
  const [activeTab, setActiveTab] = useState<"explain" | "refactor" | "tests">(
    "explain"
  );

  const {
    explainCode: explainCodeAction,
    isLoading: explainLoading,
    error: explainError,
    result: explainResult,
    clearError: clearExplainError,
    clearAll: clearExplainAll,
  } = useExplainCode();

  const {
    refactorCode: refactorCodeAction,
    isLoading: refactorLoading,
    error: refactorError,
    result: refactorResult,
    clearError: clearRefactorError,
    clearAll: clearRefactorAll,
  } = useRefactorCode();

  const {
    generateTests: generateTestsAction,
    isLoading: testsLoading,
    error: testsError,
    result: testsResult,
    clearError: clearTestsError,
    clearAll: clearTestsAll,
  } = useGenerateTests();

  const isLoading = explainLoading || refactorLoading || testsLoading;
  const currentError = explainError || refactorError || testsError;

  const handleExplain = useCallback(async () => {
    if (!code.trim()) {
      clearExplainError();
      return;
    }

    setActiveTab("explain");
    await explainCodeAction({
      code: code.trim(),
      language: language || undefined,
    });
  }, [code, language, explainCodeAction, clearExplainError]);

  const handleRefactor = useCallback(async () => {
    if (!code.trim()) {
      clearRefactorError();
      return;
    }

    setActiveTab("refactor");
    await refactorCodeAction({
      code: code.trim(),
      language: language || undefined,
      goal: "improve readability and maintainability",
    });
  }, [code, language, refactorCodeAction, clearRefactorError]);

  const handleGenerateTests = useCallback(async () => {
    if (!code.trim()) {
      clearTestsError();
      return;
    }

    setActiveTab("tests");
    await generateTestsAction({
      code: code.trim(),
      language: language || undefined,
      test_framework: "pytest",
    });
  }, [code, language, generateTestsAction, clearTestsError]);

  const handleReset = useCallback(() => {
    setCode("");
    setLanguage("");
    setActiveTab("explain");
    clearExplainAll();
    clearRefactorAll();
    clearTestsAll();
  }, [clearExplainAll, clearRefactorAll, clearTestsAll]);

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
                  onRefactor={handleRefactor}
                  onGenerateTests={handleGenerateTests}
                  onReset={handleReset}
                  disabled={isLoading}
                />
              </div>

              <div className="output-section">
                {isLoading && <LoadingSpinner />}
                {currentError && (
                  <div className="error-container">
                    <h3>❌ Error</h3>
                    <p>{currentError}</p>
                    <button
                      onClick={() => {
                        clearExplainError();
                        clearRefactorError();
                        clearTestsError();
                      }}
                      className="btn btn-secondary"
                    >
                      Clear Error
                    </button>
                  </div>
                )}

                {/* Tab Navigation */}
                <div className="tabs">
                  <button
                    className={`tab ${activeTab === "explain" ? "active" : ""}`}
                    onClick={() => setActiveTab("explain")}
                  >
                    🤖 Explain
                  </button>
                  <button
                    className={`tab ${
                      activeTab === "refactor" ? "active" : ""
                    }`}
                    onClick={() => setActiveTab("refactor")}
                  >
                    🔧 Refactor
                  </button>
                  <button
                    className={`tab ${activeTab === "tests" ? "active" : ""}`}
                    onClick={() => setActiveTab("tests")}
                  >
                    🧪 Tests
                  </button>
                </div>

                {/* Tab Content */}
                <div className="tab-content">
                  {activeTab === "explain" && explainResult && !isLoading && (
                    <ExplanationOutput result={explainResult} />
                  )}
                  {activeTab === "refactor" && refactorResult && !isLoading && (
                    <RefactorOutput result={refactorResult} />
                  )}
                  {activeTab === "tests" && testsResult && !isLoading && (
                    <TestsOutput result={testsResult} />
                  )}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ErrorBoundary>
  );
}
