import { BarChart3, Clock3 } from "lucide-react";

function PerformanceCard() {
  return (
    <article className="performance-card">
      <div className="performance-card-header">
        <div>
          <p className="card-eyebrow">PORTFOLIO PERFORMANCE</p>
          <h2>Performance over time</h2>
          <p className="card-description">
            Track how your portfolio evolves across different periods.
          </p>
        </div>

        <div className="performance-icon">
          <BarChart3 size={18} strokeWidth={1.8} />
        </div>
      </div>

      <div className="performance-chart">
        <div className="chart-grid">
          <span />
          <span />
          <span />
          <span />
        </div>

        <div className="chart-empty-state">
          <div className="chart-empty-icon">
            <Clock3 size={22} strokeWidth={1.6} />
          </div>

          <h3>Building your history</h3>

          <p>
            PortfolioPulse will start collecting portfolio snapshots
            so you can see your performance over time.
          </p>
        </div>
      </div>

      <div className="performance-footer">
        <div className="performance-periods">
          {["1D", "1W", "1M", "3M", "6M", "1Y"].map(
            (period, index) => (
              <button
                key={period}
                className={`period-button ${
                  index === 0 ? "active" : ""
                }`}
                disabled
              >
                {period}
              </button>
            )
          )}
        </div>

        <span className="history-status">
          History not available yet
        </span>
      </div>
    </article>
  );
}

export default PerformanceCard;