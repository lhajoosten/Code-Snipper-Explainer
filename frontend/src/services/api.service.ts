import { ExplainCodeRequest, ExplainCodeResponse, RefactorCodeRequest, RefactorCodeResponse, GenerateTestsRequest, GenerateTestsResponse, ApiError, HealthResponse } from '../types';

// Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT = 30000; // 30 seconds

/**
 * Custom error class for API-related errors
 */
export class ApiServiceError extends Error {
    constructor(
        message: string,
        public statusCode?: number,
        public apiError?: ApiError
    ) {
        super(message);
        this.name = 'ApiServiceError';
    }
}

/**
 * Request cache for deduplication
 */
class RequestCache {
    private cache = new Map<string, Promise<any>>();
    private readonly TTL = 5 * 60 * 1000; // 5 minutes

    private generateKey(endpoint: string, options: RequestInit): string {
        return `${endpoint}:${JSON.stringify(options.body || '')}`;
    }

    get<T>(endpoint: string, options: RequestInit): Promise<T> | null {
        const key = this.generateKey(endpoint, options);
        return this.cache.get(key) || null;
    }

    set<T>(endpoint: string, options: RequestInit, promise: Promise<T>): Promise<T> {
        const key = this.generateKey(endpoint, options);
        this.cache.set(key, promise);

        // Auto-cleanup after TTL
        setTimeout(() => {
            this.cache.delete(key);
        }, this.TTL);

        return promise;
    }

    clear(): void {
        this.cache.clear();
    }
}

/**
 * HTTP client wrapper with error handling, timeout support, and caching
 */
class HttpClient {
    private baseUrl: string;
    private timeout: number;
    private cache = new RequestCache();

    constructor(baseUrl: string, timeout: number = API_TIMEOUT) {
        this.baseUrl = baseUrl;
        this.timeout = timeout;
    }

    private async request<T>(
        endpoint: string,
        options: RequestInit = {},
        useCache: boolean = false
    ): Promise<T> {
        // Check cache for GET requests or when explicitly requested
        if (useCache || options.method === 'GET') {
            const cached = this.cache.get<T>(endpoint, options);
            if (cached) {
                return cached;
            }
        }

        const url = `${this.baseUrl}${endpoint}`;

        // Setup timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        const requestPromise = (async (): Promise<T> => {
            try {
                const response = await fetch(url, {
                    ...options,
                    signal: controller.signal,
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers,
                    },
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    await this.handleErrorResponse(response);
                }

                return await response.json();
            } catch (error) {
                clearTimeout(timeoutId);

                if (error instanceof DOMException && error.name === 'AbortError') {
                    throw new ApiServiceError('Request timed out', 408);
                }

                if (error instanceof ApiServiceError) {
                    throw error;
                }

                throw new ApiServiceError(
                    `Network error: ${error instanceof Error ? error.message : 'Unknown error'}`
                );
            }
        })();

        // Cache the promise for deduplication
        if (useCache || options.method === 'GET') {
            return this.cache.set(endpoint, options, requestPromise);
        }

        return requestPromise;
    }

    private async handleErrorResponse(response: Response): Promise<never> {
        let apiError: ApiError;

        try {
            apiError = await response.json();
        } catch {
            // Fallback if response is not JSON
            apiError = {
                type: 'unknown_error',
                message: response.statusText || 'Unknown error occurred',
            };
        }

        const errorMessage = this.getErrorMessage(response.status, apiError);
        throw new ApiServiceError(errorMessage, response.status, apiError);
    }

    private getErrorMessage(statusCode: number, apiError: ApiError): string {
        // Map common HTTP status codes to user-friendly messages
        switch (statusCode) {
            case 400:
                return apiError.message || 'Invalid request. Please check your input.';
            case 401:
                return 'Authentication required. Please log in.';
            case 403:
                return 'You do not have permission to perform this action.';
            case 404:
                return 'The requested resource was not found.';
            case 429:
                return 'Too many requests. Please wait a moment and try again.';
            case 500:
                return 'Server error. Please try again later.';
            case 502:
            case 503:
            case 504:
                return 'Service temporarily unavailable. Please try again later.';
            default:
                return apiError.message || `Request failed (${statusCode})`;
        }
    }

    async post<T>(endpoint: string, data?: unknown, useCache: boolean = false): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'POST',
            body: data ? JSON.stringify(data) : undefined,
        }, useCache);
    }

    async get<T>(endpoint: string, useCache: boolean = true): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'GET',
        }, useCache);
    }

    clearCache(): void {
        this.cache.clear();
    }
}

// Create HTTP client instance
const httpClient = new HttpClient(API_BASE_URL);

/**
 * API service for code explanation endpoints
 */
export class ApiService {
    /**
     * Explain code using AI (with caching for identical requests)
     */
    async explainCode(request: ExplainCodeRequest): Promise<ExplainCodeResponse> {
        // Use cache for POST requests with same content (explanations are deterministic)
        return httpClient.post<ExplainCodeResponse>('/api/v1/explain/', request, true);
    }

    /**
     * Refactor code using AI (with caching for identical requests)
     */
    async refactorCode(request: RefactorCodeRequest): Promise<RefactorCodeResponse> {
        // Use cache for POST requests with same content (refactoring suggestions are deterministic)
        return httpClient.post<RefactorCodeResponse>('/api/v1/refactor/', request, true);
    }

    /**
     * Generate tests for code using AI (with caching for identical requests)
     */
    async generateTests(request: GenerateTestsRequest): Promise<GenerateTestsResponse> {
        // Use cache for POST requests with same content (test generation is deterministic)
        return httpClient.post<GenerateTestsResponse>('/api/v1/tests/', request, true);
    }

    /**
     * Health check endpoint
     */
    async getHealth(): Promise<HealthResponse> {
        return httpClient.get<HealthResponse>('/health');
    }

    /**
     * Legacy ping endpoint
     */
    async ping(): Promise<{ status: string; timestamp: string }> {
        return httpClient.get('/ping');
    }

    /**
     * Clear API cache
     */
    clearCache(): void {
        httpClient.clearCache();
    }
}

// Export singleton instance
export const apiService = new ApiService();

// Export main function for convenience (following your existing pattern)
export async function explainCodeApi(request: ExplainCodeRequest): Promise<ExplainCodeResponse> {
    return apiService.explainCode(request);
}

export async function refactorCodeApi(request: RefactorCodeRequest): Promise<RefactorCodeResponse> {
    return apiService.refactorCode(request);
}

export async function generateTestsApi(request: GenerateTestsRequest): Promise<GenerateTestsResponse> {
    return apiService.generateTests(request);
}

// Export health check for Header component status indicator
export async function healthCheckApi(): Promise<HealthResponse> {
    return apiService.getHealth();
}

// Legacy ping export
export async function pingApi(): Promise<{ status: string; timestamp: string }> {
    return apiService.ping();
}