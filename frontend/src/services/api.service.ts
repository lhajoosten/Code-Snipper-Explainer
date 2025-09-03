// API types following backend DTOs
interface ExplainCodeRequest {
    code: string;
    language?: string;
}

interface ExplainCodeResponse {
    explanation: string;
    line_count: number;
    character_count: number;
    provider: string;
    placeholder: boolean;
}

interface ApiError {
    type: string;
    message: string;
    details?: Record<string, unknown>;
}

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
 * HTTP client wrapper with error handling and timeout support
 */
class HttpClient {
    private baseUrl: string;
    private timeout: number;

    constructor(baseUrl: string, timeout: number = API_TIMEOUT) {
        this.baseUrl = baseUrl;
        this.timeout = timeout;
    }

    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;

        // Setup timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

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

    async post<T>(endpoint: string, data?: unknown): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'POST',
            body: data ? JSON.stringify(data) : undefined,
        });
    }

    async get<T>(endpoint: string): Promise<T> {
        return this.request<T>(endpoint, {
            method: 'GET',
        });
    }
}

// Create HTTP client instance
const httpClient = new HttpClient(API_BASE_URL);

/**
 * API service for code explanation endpoints
 */
export class ApiService {
    /**
     * Explain code using AI
     */
    async explainCode(request: ExplainCodeRequest): Promise<ExplainCodeResponse> {
        return httpClient.post<ExplainCodeResponse>('/api/v1/explain/', request);
    }

    /**
     * Health check endpoint
     */
    async ping(): Promise<{ status: string; timestamp: string }> {
        return httpClient.get('/ping');
    }
}

// Export singleton instance
export const apiService = new ApiService();

// Export main function for convenience (following your existing pattern)
export async function explainCodeApi(request: ExplainCodeRequest): Promise<ExplainCodeResponse> {
    return apiService.explainCode(request);
}

// Export health check for Header component status indicator
export async function pingApi(): Promise<{ status: string; timestamp: string }> {
    return apiService.ping();
}