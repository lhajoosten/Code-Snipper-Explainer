import { TabType } from "../hooks/useKeyboardShortcuts";

export interface EmptyStateProps {
  activeTab: TabType;
  onAction: () => void;
  disabled?: boolean;
}

export function EmptyState({ activeTab, onAction, disabled }: EmptyStateProps) {
  const getTabIcon = (tab: string) => {
    switch (tab) {
      case "explain":
        return "🤖";
      case "refactor":
        return "🔧";
      case "tests":
        return "🧪";
      default:
        return "";
    }
  };

  const getTabTitle = (tab: TabType) => {
    switch (tab) {
      case "explain":
        return "explain";
      case "refactor":
        return "refactor";
      case "tests":
        return "generate tests";
      default:
        return "";
    }
  };

  const getTabDescription = (tab: TabType) => {
    switch (tab) {
      case "explain":
        return "Paste your code above and click 'Explain Code' to get started";
      case "refactor":
        return "Paste your code above and click 'Refactor Code' to improve it";
      case "tests":
        return "Paste your code above and click 'Generate Tests' to create test cases";
      default:
        return "";
    }
  };

  const getButtonText = (tab: TabType) => {
    switch (tab) {
      case "explain":
        return "🤖 Explain Code";
      case "refactor":
        return "🔧 Refactor Code";
      case "tests":
        return "🧪 Generate Tests";
      default:
        return "";
    }
  };

  return (
    <div className="empty-state">
      <div className="empty-state-icon">{getTabIcon(activeTab)}</div>
      <h3>Ready to {getTabTitle(activeTab)}</h3>
      <p>{getTabDescription(activeTab)}</p>
      <div className="empty-state-actions">
        <button
          onClick={onAction}
          className="btn btn-primary"
          disabled={disabled}
        >
          {getButtonText(activeTab)}
        </button>
      </div>
    </div>
  );
}
