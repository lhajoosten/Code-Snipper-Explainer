export function Header() {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="brand">
            <h1 className="brand-title">
              <span className="brand-icon">🤖</span>
              AI Code Assistant
            </h1>
            <span className="brand-subtitle">Explain, Analyze, Understand</span>
          </div>

          <div className="header-nav">
            <div className="status-indicator">
              <span className="status-dot"></span>
              <span className="status-text">Ready</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
