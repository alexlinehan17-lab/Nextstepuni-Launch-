/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';

interface ToolErrorBoundaryProps {
  children: React.ReactNode;
  toolName: string;
  onBack: () => void;
}

interface ToolErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ToolErrorBoundary extends React.Component<ToolErrorBoundaryProps, ToolErrorBoundaryState> {
  constructor(props: ToolErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ToolErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    console.error(`[ToolErrorBoundary] ${this.props.toolName} crashed:`, error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center min-h-[50vh] px-6">
          <div className="text-center max-w-sm">
            <div className="w-14 h-14 mx-auto mb-5 rounded-2xl bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-zinc-400 dark:text-zinc-500">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
            </div>
            <h2 className="font-serif text-xl font-semibold text-zinc-800 dark:text-white mb-2">
              Something went wrong with {this.props.toolName}
            </h2>
            <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-6">
              This tool ran into an issue. Your progress is safe — head back and try again.
            </p>
            {this.state.error && (
              <p className="text-xs text-zinc-400 dark:text-zinc-600 mb-6 font-mono break-all">
                {this.state.error.message}
              </p>
            )}
            <button
              onClick={this.props.onBack}
              className="px-6 py-2.5 rounded-xl text-sm font-semibold text-white transition-colors"
              style={{ backgroundColor: '#2A7D6F' }}
            >
              Back to Innovation Zone
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ToolErrorBoundary;
