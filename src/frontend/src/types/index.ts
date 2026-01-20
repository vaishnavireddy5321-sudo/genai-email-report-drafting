/**
 * Type definitions for the application
 */

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'USER' | 'ADMIN';
  created_at: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export interface Document {
  id: number;
  doc_type: 'email' | 'report';
  title?: string | null;
  tone: string;
  structure?: string | null;
  created_at: string;

  // Backend fields (available on document detail and generation responses)
  user_id?: number;
  prompt_input?: string | null;
  content?: string;

  // Backend history list includes a preview, not full content
  content_preview?: string;
}

export interface DocumentsState {
  items: Document[];
  loading: boolean;
  error: string | null;
  currentDocument: Document | null;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface GenerateDocumentRequest {
  doc_type: 'email' | 'report';
  tone: string;
  input_context: string;
}

export interface ApiError {
  error: string;
  details?: string;
}

export interface AuditLog {
  id: number;
  user_id: number | null;
  username: string | null;
  action: string;
  entity_type: string | null;
  entity_id: number | null;
  request_context_id: string | null;
  details: string | null;
  created_at: string;
}

export interface AdminSummary {
  total_users: number;
  total_documents: number;
  documents_last_24h: number;
  recent_events_count: number;
}
