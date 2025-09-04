import { TabType } from "../hooks/useKeyboardShortcuts";
import { TabNavigation } from "./TabNavigation";
import { EmptyState } from "./EmptyState";
import { ErrorDisplay } from "./ErrorDisplay";
import { ExplanationOutput } from "./ExplanationOutput";
import { RefactorOutput } from "./RefactorOutput";
import { TestsOutput } from "./TestsOutput";
import { LoadingSpinner } from "./LoadingSpinner";

export interface OutputSectionProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
  isLoading: boolean;
  error: string | null;
  onErrorDismiss: () => void;
  onRetry: () => void;
  onQuickAction: () => void;
  code: string;
  explainResult: any;
  refactorResult: any;
  testsResult: any;
}

export function OutputSection({
  activeTab,
  onTabChange,
  isLoading,
  error,
  onErrorDismiss,
  onRetry,
  onQuickAction,
  code,
  explainResult,
  refactorResult,
  testsResult,
}: OutputSectionProps) {
  const hasResult = (tab: TabType) => {
    switch (tab) {
      case "explain":
        return !!explainResult;
      case "refactor":
        return !!refactorResult;
      case "tests":
        return !!testsResult;
      default:
        return false;
    }
  };

  const renderTabContent = () => {
    if (activeTab === "explain" && explainResult && !isLoading) {
      return <ExplanationOutput result={explainResult} />;
    }
    if (activeTab === "refactor" && refactorResult && !isLoading) {
      return <RefactorOutput result={refactorResult} />;
    }
    if (activeTab === "tests" && testsResult && !isLoading) {
      return <TestsOutput result={testsResult} />;
    }
    return null;
  };

  return (
    <div className="output-section">
      {isLoading && (
        <div className="loading-overlay">
          <LoadingSpinner />
          <div className="loading-text">
            <p>Analyzing your code...</p>
            <small>This may take a few seconds</small>
          </div>
        </div>
      )}

      {error && (
        <ErrorDisplay
          error={error}
          onDismiss={onErrorDismiss}
          onRetry={onRetry}
          retryDisabled={!code.trim() || isLoading}
        />
      )}

      <TabNavigation
        activeTab={activeTab}
        onTabChange={onTabChange}
        disabled={isLoading}
      />

      <div className="tab-content">
        {renderTabContent()}

        {!isLoading && !error && !hasResult(activeTab) && (
          <EmptyState
            activeTab={activeTab}
            onAction={onQuickAction}
            disabled={!code.trim() || isLoading}
          />
        )}
      </div>
    </div>
  );
}
