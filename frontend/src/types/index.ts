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

export interface RefactorCodeRequest {
    code: string;
    language?: string;
    goal?: string;
}

export interface RefactorCodeResponse {
    refactored_code: string;
    explanation: string;
    improvements: string[];
    line_count: number;
    character_count: number;
    provider: string;
    placeholder: boolean;
}

export interface GenerateTestsRequest {
    code: string;
    language?: string;
    test_framework?: string;
}

export interface GenerateTestsResponse {
    test_code: string;
    test_framework: string;
    test_cases: string[];
    setup_instructions?: string;
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
    refactorResult: RefactorCodeResponse | null;
    testResult: GenerateTestsResponse | null;
    activeTab: 'explain' | 'refactor' | 'tests';
}

// Component prop types
export interface CodeInputProps {
    code: string;
    language: string;
    onCodeChange: (code: string) => void;
    onLanguageChange: (language: string) => void;
    onExplain: () => void;
    onRefactor: () => void;
    onGenerateTests: () => void;
    onReset: () => void;
    disabled?: boolean;
    hasUnsavedChanges?: boolean;
}

export interface ExplanationOutputProps {
    result: ExplainCodeResponse;
}

export interface RefactorOutputProps {
    result: RefactorCodeResponse;
}

export interface TestsOutputProps {
    result: GenerateTestsResponse;
}

// Language support
export interface SupportedLanguage {
    value: string;
    label: string;
    extension?: string;
}
