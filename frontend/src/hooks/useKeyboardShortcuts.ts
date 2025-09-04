import { useEffect, useCallback } from "react";

export type TabType = "explain" | "refactor" | "tests";

export interface UseKeyboardShortcutsProps {
    activeTab: TabType;
    setActiveTab: (tab: TabType) => void;
    isLoading: boolean;
    code: string;
    onQuickAction: () => void;
}

export function useKeyboardShortcuts({
    activeTab,
    setActiveTab,
    isLoading,
    code,
    onQuickAction,
}: UseKeyboardShortcutsProps) {
    const handleKeyDown = useCallback(
        (e: KeyboardEvent) => {
            if (e.ctrlKey || e.metaKey) {
                switch (e.key) {
                    case "1":
                        e.preventDefault();
                        setActiveTab("explain");
                        break;
                    case "2":
                        e.preventDefault();
                        setActiveTab("refactor");
                        break;
                    case "3":
                        e.preventDefault();
                        setActiveTab("tests");
                        break;
                    case "Enter":
                        if (e.shiftKey && !isLoading && code.trim()) {
                            e.preventDefault();
                            onQuickAction();
                        }
                        break;
                }
            }
        },
        [activeTab, setActiveTab, isLoading, code, onQuickAction]
    );

    useEffect(() => {
        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [handleKeyDown]);
}
