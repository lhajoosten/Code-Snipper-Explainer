import { useState, useCallback, useRef } from 'react';
import { refactorCodeApi, ApiServiceError } from '../services/api.service';
import { RefactorCodeRequest, RefactorCodeResponse } from '../types';

interface UseRefactorCodeResult {
    isLoading: boolean;
    error: string | null;
    result: RefactorCodeResponse | null;
    refactorCode: (request: RefactorCodeRequest) => Promise<void>;
    clearError: () => void;
    clearResult: () => void;
    clearAll: () => void;
}

export function useRefactorCode(): UseRefactorCodeResult {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<RefactorCodeResponse | null>(null);

    // Track current request to prevent race conditions
    const currentRequestRef = useRef<Promise<void> | null>(null);

    const refactorCode = useCallback(async (request: RefactorCodeRequest) => {
        // Validate input
        if (!request.code?.trim()) {
            setError('Code cannot be empty');
            return;
        }

        setIsLoading(true);
        setError(null);
        setResult(null);

        const requestPromise = (async () => {
            try {
                const response = await refactorCodeApi(request);
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
                console.error('Failed to refactor code:', err);
            }
        })();

        currentRequestRef.current = requestPromise;

        try {
            await requestPromise;
        } finally {
            // Only update loading state if this is still the current request
            if (currentRequestRef.current === requestPromise) {
                setIsLoading(false);
                currentRequestRef.current = null;
            }
        }
    }, []);

    const clearError = useCallback(() => setError(null), []);
    const clearResult = useCallback(() => setResult(null), []);
    const clearAll = useCallback(() => {
        setError(null);
        setResult(null);
        currentRequestRef.current = null;
    }, []);

    return {
        isLoading,
        error,
        result,
        refactorCode,
        clearError,
        clearResult,
        clearAll,
    };
}
