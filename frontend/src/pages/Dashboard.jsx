import { RefreshCw } from "lucide-react";
import PortfolioSummary from "../components/portfolio/PortfolioSummary";
import PerformanceCard from "../components/portfolio/PerformanceCard";
import HoldingsTable from "../components/portfolio/HoldingsTable";
import AllocationCard from "../components/portfolio/AllocationCard";
import Notification from "../components/ui/Notification";

function Dashboard({
    portfolio,
    onRefresh,
    refreshing,
    lastUpdated,
    notification,
    onCloseNotification,
    onSelectHolding,
}) {
    return (
        <>
            <Notification
                notification={notification}
                onClose={onCloseNotification}
            />
            <section className="page-header">
                <div>
                    <p className="eyebrow">OVERVIEW</p>

                    <h1>Good evening, Maharsh.</h1>

                    <p className="page-description">
                        Your portfolio at a glance.
                    </p>
                </div>

                <div className="dashboard-actions">
                    <div className="sync-info">
                        <span className="sync-dot" />

                        <span>Portfolio data</span>

                        {lastUpdated && (
                            <>
                                <span className="sync-divider" />

                                <span className="last-updated">
                                    Updated{" "}
                                    {lastUpdated.toLocaleTimeString("en-IN", {
                                        hour: "numeric",
                                        minute: "2-digit",
                                    })}
                                </span>
                            </>
                        )}
                    </div>

                    <button
                        className="refresh-button"
                        onClick={onRefresh}
                        disabled={refreshing}
                    >
                        <RefreshCw
                            size={14}
                            strokeWidth={2}
                            className={refreshing ? "refresh-icon spinning" : ""}
                        />

                        <span>
                            {refreshing ? "Refreshing..." : "Refresh"}
                        </span>
                    </button>
                </div>
            </section>

            <PortfolioSummary portfolio={portfolio} />

            <section className="dashboard-analytics">
                <PerformanceCard />

                <AllocationCard holdings={portfolio.holdings} />
            </section>

            <section className="dashboard-section">
                <div className="section-heading">
                    <div>
                        <h2>Your holdings</h2>

                        <p>
                            Stocks currently held in your Groww portfolio.
                        </p>
                    </div>

                    <div className="holding-count">
                        <span className="holding-count-dot" />

                        <span>
                            {portfolio.holdings.length}{" "}
                            {portfolio.holdings.length === 1
                                ? "holding"
                                : "holdings"}
                        </span>
                    </div>
                </div>

                <HoldingsTable
                    holdings={portfolio.holdings}
                    onSelectHolding={onSelectHolding}
                />
            </section>
        </>
    );
}

export default Dashboard;