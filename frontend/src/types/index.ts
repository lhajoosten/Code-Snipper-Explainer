// Shared types that match backend DTOs
export interface ExplainCodeRequest {
    code: string;
    language?: string;
}

export interface ExplainCodeResponse {
    explanation: string;
    line_count: number;
    character_count: number;
    provider: string;
    placeholder: boolean;
}

export interface ApiError {
    type: string;
    message: string;
    details?: Record<string, unknown>;
}

export interface HealthResponse {
    status: string;
    version: string;
    api_version: string;
    ai_provider: string;
    environment: string;
    timestamp: string;
}

// UI State types
export interface AppState {
    code: string;
    language: string;
    isLoading: boolean;
    error: string | null;
    result: ExplainCodeResponse | null;
}

// Component prop types
export interface CodeInputProps {
    code: string;
    language: string;
    onCodeChange: (code: string) => void;
    onLanguageChange: (language: string) => void;
    onExplain: () => void;
    onReset: () => void;
    disabled?: boolean;
}

export interface ExplanationOutputProps {
    result: ExplainCodeResponse;
}

// Language support
export interface SupportedLanguage {
    value: string;
    label: string;
    extension?: string;
}
