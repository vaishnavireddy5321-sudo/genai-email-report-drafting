/**
 * API client for backend communication
 */

import type {
  User,
  LoginCredentials,
  RegisterData,
  GenerateDocumentRequest,
  Document,
  ApiError,
  AdminSummary,
  AuditLog,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

/**
 * Custom error class for API errors
 */
export class ApiClientError extends Error {
  statusCode?: number;
  details?: string;

  constructor(
    message: string,
    statusCode?: number,
    details?: string
  ) {
    super(message);
    this.name = 'ApiClientError';
    this.statusCode = statusCode;
    this.details = details;
  }
}

/**
 * Get stored JWT token
 */
export const getToken = (): string | null => {
  return localStorage.getItem('token');
};

/**
 * Store JWT token
 */
export const setToken = (token: string): void => {
  localStorage.setItem('token', token);
};

/**
 * Remove JWT token
 */
export const removeToken = (): void => {
  localStorage.removeItem('token');
};

/**
 * Make authenticated API request
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // Add custom headers
  if (options.headers) {
    Object.entries(options.headers).forEach(([key, value]) => {
      if (typeof value === 'string') {
        headers[key] = value;
      }
    });
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorMessage = 'An error occurred';
    let errorDetails: string | undefined;

    try {
      const errorData: ApiError = await response.json();
      errorMessage = errorData.error || errorMessage;
      errorDetails = errorData.details;
    } catch {
      // If JSON parsing fails, use status text
      errorMessage = response.statusText || errorMessage;
    }

    throw new ApiClientError(errorMessage, response.status, errorDetails);
  }

  return response.json();
}

/**
 * Authentication API
 */
export const authApi = {
  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<{ access_token: string; user: User }> {
    const response = await apiRequest<{ access_token: string; user: User }>(
      '/auth/login',
      {
        method: 'POST',
        body: JSON.stringify(credentials),
      }
    );
    setToken(response.access_token);
    return response;
  },

  /**
   * Register new user
   */
  async register(data: RegisterData): Promise<{ access_token: string; user: User }> {
    const response = await apiRequest<{ access_token: string; user: User }>(
      '/auth/register',
      {
        method: 'POST',
        body: JSON.stringify(data),
      }
    );
    setToken(response.access_token);
    return response;
  },

  /**
   * Get current user profile
   */
  async getProfile(): Promise<{ user: User }> {
    return apiRequest<{ user: User }>('/auth/me');
  },

  /**
   * Logout (client-side only)
   */
  logout(): void {
    removeToken();
  },
};

/**
 * Documents API
 */
export const documentsApi = {
  /**
   * Generate a document (email or report)
   */
  async generate(request: GenerateDocumentRequest): Promise<{ document: Document }> {
    if (request.doc_type === 'email') {
      const response = await apiRequest<{ document: Document }>(
        '/documents/email:generate',
        {
          method: 'POST',
          body: JSON.stringify({
            context: request.input_context,
            tone: request.tone,
          }),
        }
      );

      return response;
    }

    const response = await apiRequest<{ document: Document }>(
      '/documents/report:generate',
      {
        method: 'POST',
        body: JSON.stringify({
          topic: request.input_context,
          tone: request.tone,
          structure: 'detailed',
        }),
      }
    );

    return response;
  },

  /**
   * Get user's document history
   */
  async getHistory(params?: {
    limit?: number;
    offset?: number;
    doc_type?: 'email' | 'report';
  }): Promise<{ documents: Document[]; total: number; limit: number; offset: number; has_more: boolean }> {
    const queryParams = new URLSearchParams();
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());
    if (params?.doc_type) queryParams.append('doc_type', params.doc_type);

    const query = queryParams.toString();
    const endpoint = query ? `/history?${query}` : '/history';

    return apiRequest<{ documents: Document[]; total: number; limit: number; offset: number; has_more: boolean }>(endpoint);
  },

  /**
   * Get full document details (content, prompt_input)
   */
  async getDetail(documentId: number): Promise<{ document: Document }> {
    return apiRequest<{ document: Document }>(`/history/${documentId}`);
  },
};

/**
 * Admin API
 */
export const adminApi = {
  /**
   * Get system summary metrics
   */
  async getSummary(): Promise<AdminSummary> {
    return apiRequest<AdminSummary>('/admin/summary');
  },

  /**
   * Get audit logs
   */
  async getAuditLogs(params?: {
    limit?: number;
    offset?: number;
  }): Promise<{ audit_logs: AuditLog[]; total: number; limit: number; offset: number }> {
    const queryParams = new URLSearchParams();
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());

    const query = queryParams.toString();
    const endpoint = query ? `/admin/audit-logs?${query}` : '/admin/audit-logs';

    return apiRequest<{ audit_logs: AuditLog[]; total: number; limit: number; offset: number }>(endpoint);
  },
};
