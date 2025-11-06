/**
 * Error Boundary Component
 * Catches and displays React errors gracefully
 */

import React from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log error to console for debugging
    console.error('Error caught by boundary:', error, errorInfo);

    this.setState({
      error,
      errorInfo,
    });

    // You could also log to an error reporting service here
    if (window.nyxAPI?.error) {
      window.nyxAPI.error('React Error:', error.toString(), errorInfo.componentStack);
    }
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });

    // Optional: Call parent reset callback
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-nyx-dark p-6">
          <div className="glass max-w-2xl w-full p-8 rounded-lg border border-nyx-error">
            {/* Error Icon */}
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-nyx-error/20 rounded-full">
                <AlertTriangle className="w-8 h-8 text-nyx-error" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">
                  Oops! Something went wrong
                </h1>
                <p className="text-gray-400 mt-1">
                  The application encountered an unexpected error
                </p>
              </div>
            </div>

            {/* Error Details */}
            {this.state.error && (
              <div className="mb-6">
                <div className="bg-nyx-dark/50 p-4 rounded-lg border border-gray-700">
                  <p className="font-mono text-sm text-nyx-error mb-2">
                    {this.state.error.toString()}
                  </p>
                  {process.env.NODE_ENV === 'development' && this.state.errorInfo && (
                    <details className="mt-3">
                      <summary className="text-gray-400 cursor-pointer hover:text-white transition-colors">
                        Stack Trace (Development Only)
                      </summary>
                      <pre className="mt-2 text-xs text-gray-500 overflow-auto max-h-48">
                        {this.state.errorInfo.componentStack}
                      </pre>
                    </details>
                  )}
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                onClick={this.handleReset}
                className="flex items-center gap-2 px-6 py-3 bg-nyx-accent hover:bg-nyx-accent-hover rounded-lg transition-colors"
              >
                <RefreshCw className="w-5 h-5" />
                Try Again
              </button>

              <button
                onClick={() => window.location.reload()}
                className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
              >
                Reload Application
              </button>
            </div>

            {/* Help Text */}
            <div className="mt-6 pt-6 border-t border-gray-700">
              <p className="text-sm text-gray-400">
                If this problem persists, please try:
              </p>
              <ul className="list-disc list-inside text-sm text-gray-500 mt-2 space-y-1">
                <li>Reloading the application</li>
                <li>Clearing your cache</li>
                <li>Checking the console for more details</li>
                <li>Reporting the issue on GitHub</li>
              </ul>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
