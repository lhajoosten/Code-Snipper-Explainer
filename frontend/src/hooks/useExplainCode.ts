import { useState } from 'react';
import { explainCodeApi, ApiServiceError } from '../services/api.service';

interface ExplainRequest {
    code: string;
    language?: string;
}

interface ExplanationResult {
    explanation: string;
    line_count: number;
    character_count: number;
    provider: string;
    placeholder: boolean;
}

export function useExplainCode() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<ExplanationResult | null>(null);

    const explainCode = async (request: ExplainRequest) => {
        setIsLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await explainCodeApi(request);
            setResult(response);
        } catch (err) {
            let errorMessage: string;

            if (err instanceof ApiServiceError) {
                errorMessage = err.message;
            } else if (err instanceof Error) {
                errorMessage = err.message;
            } else {
                errorMessage = 'An unexpected error occurred';
            }

            setError(errorMessage);
            console.error('Failed to explain code:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const clearError = () => setError(null);
    const clearResult = () => setResult(null);

    return {
        explainCode,
        isLoading,
        error,
        result,
        clearError,
        clearResult,
    };
}