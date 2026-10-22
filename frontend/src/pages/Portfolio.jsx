
import { useEffect, useState } from "react";
import { RefreshCw, BriefcaseBusiness } from "lucide-react";
import HoldingsTable from "../components/portfolio/HoldingsTable";

function Portfolio() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");

  async function loadPortfolio(isRefresh = false) {
    if (isRefresh) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }

    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/portfolio");

      if (!response.ok) {
        throw new Error("Unable to load portfolio. Please try again.");
      }

      const data = await response.json();
      setPortfolio(data);
    } catch (err) {
      setError(
        err.message || "Unable to connect to the PortfolioPulse backend.",
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loadPortfolio();
  }, []);

  const formatCurrency = (value) =>
    new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2,
    }).format(Number(value ?? 0));

  const formatPercentage = (value) => {
    const percentage = Number(value ?? 0);
    return `${percentage > 0 ? "+" : ""}${percentage.toFixed(2)}%`;
  };

  const pnlClass = (value) => {
    const amount = Number(value ?? 0);
    if (amount > 0) return "positive";
    if (amount < 0) return "negative";
    return "";
  };

  return (
    <section className="portfolio-page">
      <header className="page-header">
        <div>
          <p className="eyebrow">YOUR INVESTMENTS</p>
          <h1>Portfolio</h1>
          <p className="page-description">
            Review your holdings, market values, and unrealized performance.
          </p>
        </div>

        <button
          className="refresh-button"
          onClick={() => loadPortfolio(true)}
          disabled={loading || refreshing}
        >
          <RefreshCw
            size={14}
            className={refreshing ? "refresh-icon spinning" : ""}
          />
          <span>{refreshing ? "Refreshing..." : "Refresh"}</span>
        </button>
      </header>

      {loading && <div className="state-card">Loading your portfolio...</div>}

      {!loading && error && (
        <div className="state-card error-state">
          <p>{error}</p>
          <button
            className="refresh-button"
            onClick={() => loadPortfolio()}
          >
            Try again
          </button>
        </div>
      )}

      {!loading && !error && portfolio && (
        <>
          <div className="portfolio-summary-grid">
            <article className="portfolio-metric-card">
              <span>Total invested</span>
              <strong>{formatCurrency(portfolio.total_invested)}</strong>
            </article>

            <article className="portfolio-metric-card">
              <span>Current value</span>
              <strong>
                {formatCurrency(portfolio.total_current_value)}
              </strong>
            </article>

            <article className="portfolio-metric-card">
              <span>Total P&amp;L</span>
              <strong className={pnlClass(portfolio.total_pnl)}>
                {formatCurrency(portfolio.total_pnl)}
              </strong>
              <small className={pnlClass(portfolio.total_pnl_percentage)}>
                {formatPercentage(portfolio.total_pnl_percentage)}
              </small>
            </article>

            <article className="portfolio-metric-card">
              <span>Holdings</span>
              <strong>{portfolio.holdings.length}</strong>
            </article>
          </div>

          <section className="dashboard-section portfolio-holdings-section">
            <div className="section-heading">
              <div>
                <h2>All holdings</h2>
                <p>
                  Current positions and unrealized profit or loss.
                </p>
              </div>
              <span className="holding-count">
                {portfolio.holdings.length}{" "}
                {portfolio.holdings.length === 1 ? "holding" : "holdings"}
              </span>
            </div>

            {portfolio.holdings.length > 0 ? (
              <HoldingsTable holdings={portfolio.holdings} />
            ) : (
              <div className="state-card">
                <BriefcaseBusiness size={24} />
                <p>No holdings found in your portfolio yet.</p>
              </div>
            )}
          </section>

          <p className="portfolio-data-note">
            Prices may be delayed or unavailable. Check each holding's price
            status before relying on its displayed market value.
          </p>
        </>
      )}
    </section>
  );
}

export default Portfolio;
