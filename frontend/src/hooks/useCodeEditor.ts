import React, { useState, useCallback, useEffect } from "react";

export interface UseCodeEditorReturn {
    code: string;
    language: string;
    hasUnsavedChanges: boolean;
    setCode: (code: string) => void;
    setLanguage: (language: string) => void;
    reset: () => void;
    markAsSaved: () => void;
}

export function useCodeEditor(): UseCodeEditorReturn {
    const [code, setCodeState] = useState(() => {
        return localStorage.getItem("code-snippet") || "";
    });

    const [language, setLanguageState] = useState(() => {
        return localStorage.getItem("code-language") || "";
    });

    const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

    // Auto-save to localStorage
    useEffect(() => {
        localStorage.setItem("code-snippet", code);
        localStorage.setItem("code-language", language);
    }, [code, language]);

    // Track unsaved changes for beforeunload
    useEffect(() => {
        const handleBeforeUnload = (e: BeforeUnloadEvent) => {
            if (hasUnsavedChanges) {
                e.preventDefault();
                e.returnValue = "";
            }
        };

        window.addEventListener("beforeunload", handleBeforeUnload);
        return () => window.removeEventListener("beforeunload", handleBeforeUnload);
    }, [hasUnsavedChanges]);

    const setCode = useCallback((newCode: string) => {
        setCodeState(newCode);
        setHasUnsavedChanges(true);
    }, []);

    const setLanguage = useCallback((newLanguage: string) => {
        setLanguageState(newLanguage);
        setHasUnsavedChanges(true);
    }, []);

    const reset = useCallback(() => {
        setCodeState("");
        setLanguageState("");
        setHasUnsavedChanges(false);
        localStorage.removeItem("code-snippet");
        localStorage.removeItem("code-language");
    }, []);

    const markAsSaved = useCallback(() => {
        setHasUnsavedChanges(false);
    }, []);

    return {
        code,
        language,
        hasUnsavedChanges,
        setCode,
        setLanguage,
        reset,
        markAsSaved,
    };
}
