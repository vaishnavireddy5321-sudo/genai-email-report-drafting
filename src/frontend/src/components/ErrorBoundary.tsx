/**
 * ErrorBoundary Component
 * 
 * A top-level React Error Boundary component that gracefully handles unhandled exceptions
 * and prevents application crashes. Provides a user-friendly error UI with recovery options.
 * 
 * @component
 * @example
 * <ErrorBoundary>
 *   <App />
 * </ErrorBoundary>
 */

import { Component, type ReactNode } from 'react';

/**
 * Props interface for ErrorBoundary component
 */
interface ErrorBoundaryProps {
  /** Child components to be wrapped and protected by the error boundary */
  children: ReactNode;
}

/**
 * State interface for ErrorBoundary component
 */
interface ErrorBoundaryState {
  /** Whether an error has been caught */
  hasError: boolean;
  /** The error object if an error was caught */
  error: Error | null;
  /** Additional error information from React */
  errorInfo: string | null;
}

/**
 * ErrorBoundary class component
 * 
 * Catches JavaScript errors anywhere in the child component tree, logs the errors,
 * and displays a fallback UI instead of crashing the entire application.
 * 
 * Must use class component as Error Boundaries require class-based lifecycle methods
 * (getDerivedStateFromError and componentDidCatch).
 */
class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  /**
   * Static lifecycle method called when an error is thrown in a descendant component.
   * Updates state to trigger fallback UI rendering.
   * 
   * @param error - The error that was thrown
   * @returns Updated state object
   */
  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    // Update state so the next render will show the fallback UI
    return {
      hasError: true,
      error,
    };
  }

  /**
   * Lifecycle method called after an error has been thrown in a descendant component.
   * Used for logging error information for debugging purposes.
   * 
   * @param error - The error that was thrown
   * @param errorInfo - Object containing component stack trace
   */
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    // Log error details to console for debugging
    console.error('ErrorBoundary caught an error:', error);
    console.error('Error component stack:', errorInfo.componentStack);

    // Store error info in state for potential display or reporting
    this.setState({
      errorInfo: errorInfo.componentStack || null,
    });

    // In production, you could send error to an error reporting service here
    // Example: logErrorToService(error, errorInfo);
  }

  /**
   * Handles page refresh to recover from error state
   */
  handleRefresh = (): void => {
    window.location.reload();
  };

  /**
   * Renders either the error fallback UI or the children components
   */
  render(): ReactNode {
    if (this.state.hasError) {
      // Render fallback UI when an error has been caught
      return (
        <div className="min-h-screen bg-linear-to-br from-slate-50 via-slate-100 to-slate-200 flex items-center justify-center p-4">
          <div className="max-w-2xl w-full">
            {/* Error Card */}
            <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden">
              {/* Header with gradient background */}
              <div className="bg-linear-to-r from-red-500 to-rose-500 p-6 text-white">
                <div className="flex items-center gap-4">
                  {/* Error Icon */}
                  <div className="shrink-0">
                    <svg
                      className="w-12 h-12"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                      />
                    </svg>
                  </div>
                  {/* Error Title */}
                  <div>
                    <h1 className="text-2xl font-bold">Something Went Wrong</h1>
                    <p className="text-red-100 mt-1">
                      We encountered an unexpected error
                    </p>
                  </div>
                </div>
              </div>

              {/* Error Details */}
              <div className="p-6 space-y-4">
                <p className="text-slate-600 leading-relaxed">
                  Don't worry! This error has been logged and our team will investigate.
                  You can try refreshing the page to continue using the application.
                </p>

                {/* Error Message Display (Development) */}
                {this.state.error && import.meta.env.DEV && (
                  <div className="mt-4">
                    <details className="group">
                      <summary className="cursor-pointer text-sm font-medium text-slate-700 hover:text-slate-900 flex items-center gap-2">
                        <span className="group-open:rotate-90 transition-transform">▶</span>
                        Error Details (Development Only)
                      </summary>
                      <div className="mt-2 p-4 bg-slate-50 rounded-lg border border-slate-200">
                        <p className="text-xs font-mono text-red-600 break-all">
                          {this.state.error.toString()}
                        </p>
                        {this.state.errorInfo && (
                          <pre className="mt-2 text-xs text-slate-600 overflow-auto max-h-40">
                            {this.state.errorInfo}
                          </pre>
                        )}
                      </div>
                    </details>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex flex-col sm:flex-row gap-3 pt-4">
                  <button
                    onClick={this.handleRefresh}
                    className="flex-1 px-6 py-3 bg-linear-to-r from-primary-500 to-primary-600 text-white rounded-lg font-medium hover:from-primary-600 hover:to-primary-700 transition shadow-lg shadow-primary-500/30 flex items-center justify-center gap-2"
                  >
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                      />
                    </svg>
                    Refresh Page
                  </button>
                  <button
                    onClick={() => window.history.back()}
                    className="flex-1 px-6 py-3 bg-slate-200 text-slate-700 rounded-lg font-medium hover:bg-slate-300 transition flex items-center justify-center gap-2"
                  >
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M10 19l-7-7m0 0l7-7m-7 7h18"
                      />
                    </svg>
                    Go Back
                  </button>
                </div>
              </div>
            </div>

            {/* Help Text */}
            <div className="mt-6 text-center">
              <p className="text-sm text-slate-500">
                If the problem persists, please contact support with the error details.
              </p>
            </div>
          </div>
        </div>
      );
    }

    // No error, render children normally
    return this.props.children;
  }
}

export default ErrorBoundary;
