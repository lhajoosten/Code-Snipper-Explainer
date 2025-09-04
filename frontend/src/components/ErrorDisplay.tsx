export interface ErrorDisplayProps {
  error: string;
  onDismiss: () => void;
  onRetry: () => void;
  retryDisabled?: boolean;
}

export function ErrorDisplay({
  error,
  onDismiss,
  onRetry,
  retryDisabled,
}: ErrorDisplayProps) {
  return (
    <div className="error-container">
      <div className="error-header">
        <span className="error-icon">❌</span>
        <h3>Processing Error</h3>
      </div>
      <p className="error-message">{error}</p>
      <div className="error-actions">
        <button onClick={onDismiss} className="btn btn-secondary">
          Dismiss
        </button>
        <button
          onClick={onRetry}
          className="btn btn-primary"
          disabled={retryDisabled}
        >
          Try Again
        </button>
      </div>
    </div>
  );
}
