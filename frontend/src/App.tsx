import React, { useState, useCallback } from "react";
import { CodeInput } from "./components/CodeInput";
import { OutputSection } from "./components/OutputSection";
import { Header } from "./components/Header";
import { ThemeToggle } from "./components/ThemeToggle";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import { useCodeEditor } from "./hooks/useCodeEditor";
import { useKeyboardShortcuts, TabType } from "./hooks/useKeyboardShortcuts";
import { useExplainCode } from "./hooks/useExplainCode";
import { useRefactorCode } from "./hooks/useRefactorCode";
import { useGenerateTests } from "./hooks/useGenerateTests";
import "./App.css";

export default function App() {
  const [activeTab, setActiveTab] = useState<TabType>("explain");

  const {
    code,
    language,
    hasUnsavedChanges,
    setCode,
    setLanguage,
    reset: resetCode,
    markAsSaved,
  } = useCodeEditor();

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

  const handleQuickAction = useCallback(() => {
    switch (activeTab) {
      case "explain":
        handleExplain();
        break;
      case "refactor":
        handleRefactor();
        break;
      case "tests":
        handleGenerateTests();
        break;
    }
  }, [activeTab]);

  const handleExplain = useCallback(async () => {
    if (!code.trim()) {
      clearExplainError();
      return;
    }

    setActiveTab("explain");
    markAsSaved();
    await explainCodeAction({
      code: code.trim(),
      language: language || undefined,
    });
  }, [code, language, explainCodeAction, clearExplainError, markAsSaved]);

  const handleRefactor = useCallback(async () => {
    if (!code.trim()) {
      clearRefactorError();
      return;
    }

    setActiveTab("refactor");
    markAsSaved();
    await refactorCodeAction({
      code: code.trim(),
      language: language || undefined,
      goal: "improve readability and maintainability",
    });
  }, [code, language, refactorCodeAction, clearRefactorError, markAsSaved]);

  const handleGenerateTests = useCallback(async () => {
    if (!code.trim()) {
      clearTestsError();
      return;
    }

    setActiveTab("tests");
    markAsSaved();
    await generateTestsAction({
      code: code.trim(),
      language: language || undefined,
      test_framework: "pytest",
    });
  }, [code, language, generateTestsAction, clearTestsError, markAsSaved]);

  const handleReset = useCallback(() => {
    resetCode();
    setActiveTab("explain");
    clearExplainAll();
    clearRefactorAll();
    clearTestsAll();
  }, [resetCode, clearExplainAll, clearRefactorAll, clearTestsAll]);

  // Setup keyboard shortcuts
  useKeyboardShortcuts({
    activeTab,
    setActiveTab,
    isLoading,
    code,
    onQuickAction: handleQuickAction,
  });

  return (
    <ThemeProvider>
      <ErrorBoundary>
        <div className="app">
          <Header />
          <div className="theme-toggle-container">
            <ThemeToggle />
          </div>

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
                    onRefactor={handleRefactor}
                    onGenerateTests={handleGenerateTests}
                    onReset={handleReset}
                    disabled={isLoading}
                    hasUnsavedChanges={hasUnsavedChanges}
                  />
                </div>

                <OutputSection
                  activeTab={activeTab}
                  onTabChange={setActiveTab}
                  isLoading={isLoading}
                  error={currentError}
                  onErrorDismiss={() => {
                    clearExplainError();
                    clearRefactorError();
                    clearTestsError();
                  }}
                  onRetry={handleQuickAction}
                  onQuickAction={handleQuickAction}
                  code={code}
                  explainResult={explainResult}
                  refactorResult={refactorResult}
                  testsResult={testsResult}
                />
              </div>
            </div>
          </main>
        </div>
      </ErrorBoundary>
    </ThemeProvider>
  );
}
