import { useEffect, useState } from "react";
import {
    RefreshCw,
    TrendingDown,
    TrendingUp,
} from "lucide-react";

function Market() {
    const [market, setMarket] = useState(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState("");

    async function loadMarket({ isRefresh = false } = {}) {
        try {
            if (isRefresh) {
                setRefreshing(true);
            } else {
                setLoading(true);
            }

            setError("");

            const response = await fetch(
                "http://127.0.0.1:8000/market"
            );

            if (!response.ok) {
                throw new Error("Unable to load market data.");
            }

            const data = await response.json();

            setMarket(data);
        } catch (err) {
            setError(err.message);
        } finally {
            if (isRefresh) {
                setRefreshing(false);
            } else {
                setLoading(false);
            }
        }
    }

    useEffect(() => {
        loadMarket();
    }, []);

    if (loading) {
        return (
            <div className="state-card">
                Loading market data...
            </div>
        );
    }

    if (error) {
        return (
            <div className="state-card error-state">
                {error}
            </div>
        );
    }

    const indianMarkets = market.instruments.filter((instrument) =>
        ["^NSEI", "^BSESN", "^NSEBANK"].includes(
            instrument.symbol
        )
    );

    const commodities = market.instruments.filter((instrument) =>
        ["GC=F", "SI=F"].includes(instrument.symbol)
    );

    const globalMarkets = market.instruments.filter((instrument) =>
        ["^GSPC", "^IXIC", "^DJI"].includes(
            instrument.symbol
        )
    );

    function MarketCard({ instrument }) {
        const isPositive =
            Number(instrument.change) >= 0;

        return (
            <article className="market-card">
                <div className="market-card-top">
                    <div>
                        <p className="market-card-label">
                            {instrument.name}
                        </p>

                        <span className="market-card-status">
                            {instrument.status}
                        </span>
                    </div>

                    <div
                        className={`market-direction ${
                            isPositive
                                ? "positive"
                                : "negative"
                        }`}
                    >
                        {isPositive ? (
                            <TrendingUp
                                size={14}
                                strokeWidth={2}
                            />
                        ) : (
                            <TrendingDown
                                size={14}
                                strokeWidth={2}
                            />
                        )}

                        <span>
                            {isPositive ? "+" : ""}
                            {instrument.change_percentage}%
                        </span>
                    </div>
                </div>

                <div className="market-card-value">
                    {Number(
                        instrument.value
                    ).toLocaleString("en-IN", {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                    })}
                </div>

                <div className="market-card-change">
                    <span>Change</span>

                    <span
                        className={
                            isPositive
                                ? "positive"
                                : "negative"
                        }
                    >
                        {isPositive ? "+" : ""}
                        {Number(
                            instrument.change
                        ).toLocaleString("en-IN", {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                        })}
                    </span>
                </div>

                <div className="market-card-footer">
                    <span>Previous close</span>

                    <span>
                        {Number(
                            instrument.previous_close
                        ).toLocaleString("en-IN", {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                        })}
                    </span>
                </div>
            </article>
        );
    }

    function MarketSection({
        title,
        description,
        instruments,
    }) {
        return (
            <section className="market-section">
                <div className="market-section-heading">
                    <div>
                        <h2>{title}</h2>

                        <p>{description}</p>
                    </div>
                </div>

                <div className="market-grid">
                    {instruments.map((instrument) => (
                        <MarketCard
                            key={instrument.symbol}
                            instrument={instrument}
                        />
                    ))}
                </div>
            </section>
        );
    }

    return (
        <>
            <section className="page-header market-page-header">
                <div>
                    <p className="eyebrow">MARKET</p>

                    <h1>Market overview.</h1>

                    <p className="page-description">
                        A snapshot of the markets that matter.
                    </p>
                </div>

                <button
                    className="refresh-button"
                    onClick={() =>
                        loadMarket({
                            isRefresh: true,
                        })
                    }
                    disabled={refreshing}
                >
                    <RefreshCw
                        size={14}
                        strokeWidth={2}
                        className={
                            refreshing
                                ? "refresh-icon spinning"
                                : ""
                        }
                    />

                    <span>
                        {refreshing
                            ? "Refreshing..."
                            : "Refresh"}
                    </span>
                </button>
            </section>

            <MarketSection
                title="Indian Markets"
                description="Major domestic equity indices."
                instruments={indianMarkets}
            />

            <MarketSection
                title="Commodities"
                description="Key commodity prices."
                instruments={commodities}
            />

            <MarketSection
                title="Global Markets"
                description="Major international equity indices."
                instruments={globalMarkets}
            />

            <div className="market-data-note">
                <span className="market-note-dot" />

                <span>
                    Market data is sourced from yfinance and may
                    be delayed.
                </span>
            </div>
        </>
    );
}

export default Market;