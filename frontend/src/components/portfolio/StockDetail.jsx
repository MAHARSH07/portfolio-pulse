import { ArrowLeft, TrendingUp } from "lucide-react";

const currencyFormatter = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 2,
});

function StockDetail({ holding, onBack }) {
    const hasMarketPrice =
        Number(holding.current_price) > 0;

    return (
        <div className="stock-detail-page">
            <button
                className="back-button"
                onClick={onBack}
            >
                <ArrowLeft
                    size={16}
                    strokeWidth={1.8}
                />

                <span>Back to overview</span>
            </button>

            <section className="stock-detail-header">
                <div className="stock-detail-identity">
                    <div className="stock-detail-avatar">
                        {holding.symbol.charAt(0)}
                    </div>

                    <div>
                        <p className="eyebrow">
                            YOUR HOLDING
                        </p>

                        <h1>{holding.symbol}</h1>

                        <p className="stock-detail-company">
                            {holding.company_name ||
                                "Company information pending"}
                        </p>
                    </div>
                </div>

                <div className="stock-detail-status">
                    <span className="sync-dot" />
                    Portfolio position
                </div>
            </section>

            <section className="stock-detail-metrics">
                <div className="detail-metric">
                    <span>Quantity</span>
                    <strong>{holding.quantity}</strong>
                </div>

                <div className="detail-metric">
                    <span>Average price</span>
                    <strong>
                        {currencyFormatter.format(
                            holding.average_price
                        )}
                    </strong>
                </div>

                <div className="detail-metric">
                    <span>Current price</span>
                    <strong>
                        {hasMarketPrice
                            ? currencyFormatter.format(
                                holding.current_price
                            )
                            : "—"}
                    </strong>
                </div>

                <div className="detail-metric">
                    <span>Current value</span>
                    <strong>
                        {hasMarketPrice
                            ? currencyFormatter.format(
                                holding.current_value
                            )
                            : "—"}
                    </strong>
                </div>

                <div
                    className={`detail-metric ${
                        hasMarketPrice
                            ? holding.pnl >= 0
                                ? "detail-metric-positive"
                                : "detail-metric-negative"
                            : ""
                    }`}
                >
                    <span>Unrealized P&L</span>

                    <strong>
                        {hasMarketPrice
                            ? `${
                                holding.pnl >= 0 ? "+" : ""
                            }${currencyFormatter.format(
                                holding.pnl
                            )}`
                            : "—"}
                    </strong>
                </div>
            </section>

            <section className="stock-detail-grid">
                <article className="stock-detail-card">
                    <div className="stock-detail-card-header">
                        <div>
                            <p className="card-eyebrow">
                                PERFORMANCE
                            </p>

                            <h2>Price & performance</h2>
                        </div>

                        <div className="detail-card-icon">
                            <TrendingUp
                                size={18}
                                strokeWidth={1.8}
                            />
                        </div>
                    </div>

                    <div className="detail-placeholder">
                        <h3>
                            Market data will appear here
                        </h3>

                        <p>
                            Live price and historical
                            performance data will be connected
                            in the next backend phase.
                        </p>
                    </div>
                </article>

                <article className="stock-detail-card">
                    <div className="stock-detail-card-header">
                        <div>
                            <p className="card-eyebrow">
                                POSITION
                            </p>

                            <h2>Your position</h2>
                        </div>
                    </div>

                    <div className="position-summary">
                        <div>
                            <span>Invested</span>

                            <strong>
                                {currencyFormatter.format(
                                    Number(
                                        holding.quantity
                                    ) *
                                        Number(
                                            holding.average_price
                                        )
                                )}
                            </strong>
                        </div>

                        <div>
                            <span>Broker</span>
                            <strong>Groww</strong>
                        </div>
                    </div>
                </article>
            </section>

            <section className="stock-detail-grid">
                <article className="stock-detail-card coming-soon-card">
                    <p className="card-eyebrow">
                        INTELLIGENCE
                    </p>

                    <h2>Latest news</h2>

                    <p>
                        Portfolio-relevant news will appear here
                        once our market intelligence pipeline is
                        connected.
                    </p>
                </article>

                <article className="stock-detail-card coming-soon-card">
                    <p className="card-eyebrow">
                        AI INSIGHT
                    </p>

                    <h2>Portfolio insight</h2>

                    <p>
                        AI-generated analysis will appear here
                        after the intelligence agent is connected.
                    </p>
                </article>
            </section>
        </div>
    );
}

export default StockDetail;