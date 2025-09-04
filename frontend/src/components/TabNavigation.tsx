import { TabType } from "../hooks/useKeyboardShortcuts";

export interface TabNavigationProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
  disabled?: boolean;
}

export function TabNavigation({
  activeTab,
  onTabChange,
  disabled,
}: TabNavigationProps) {
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

  const getTabShortcut = (tab: string) => {
    switch (tab) {
      case "explain":
        return "Ctrl+1";
      case "refactor":
        return "Ctrl+2";
      case "tests":
        return "Ctrl+3";
      default:
        return "";
    }
  };

  return (
    <div className="tabs-container">
      <div className="tabs">
        {(["explain", "refactor", "tests"] as const).map((tab) => (
          <button
            key={tab}
            className={`tab ${activeTab === tab ? "active" : ""}`}
            onClick={() => onTabChange(tab)}
            disabled={disabled}
            title={`${
              tab.charAt(0).toUpperCase() + tab.slice(1)
            } (${getTabShortcut(tab)})`}
          >
            <span className="tab-icon">{getTabIcon(tab)}</span>
            <span className="tab-label">
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </span>
            <span className="tab-shortcut">{getTabShortcut(tab)}</span>
          </button>
        ))}
      </div>

      <div className="shortcuts-hint">
        <small>
          💡 <strong>Pro tip:</strong> Use Ctrl+1/2/3 to switch tabs,
          Shift+Enter to run current action
        </small>
      </div>
    </div>
  );
}
