import { useEffect, useState } from "react";
import {
    RefreshCw,
    TrendingDown,
    TrendingUp,
    ExternalLink,
} from "lucide-react";

function Market() {
    const [market, setMarket] = useState(null);
    const [news, setNews] = useState([]);
    const [events, setEvents] = useState([]);

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

            const [
                marketResponse,
                newsResponse,
                eventsResponse,
            ] = await Promise.all([
                fetch("http://127.0.0.1:8000/market"),
                fetch("http://127.0.0.1:8000/market/news"),
                fetch("http://127.0.0.1:8000/market/events"),
            ]);

            if (!marketResponse.ok) {
                throw new Error(
                    "Unable to load market data."
                );
            }

            if (!newsResponse.ok) {
                throw new Error(
                    "Unable to load market news."
                );
            }

            if (!eventsResponse.ok) {
                throw new Error(
                    "Unable to load economic events."
                );
            }

            const marketData =
                await marketResponse.json();

            const newsData =
                await newsResponse.json();

            const eventsData =
                await eventsResponse.json();

            setMarket(marketData);
            setNews(newsData.articles ?? []);
            setEvents(eventsData.events ?? []);
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

    const indianMarkets = market.instruments.filter(
        (instrument) =>
            ["^NSEI", "^BSESN", "^NSEBANK"].includes(
                instrument.symbol
            )
    );

    const commodities = market.instruments.filter(
        (instrument) =>
            ["GC=F", "SI=F"].includes(
                instrument.symbol
            )
    );

    const globalMarkets = market.instruments.filter(
        (instrument) =>
            ["^GSPC", "^IXIC", "^DJI"].includes(
                instrument.symbol
            )
    );

    const indianNews = news.filter(
        (article) =>
            article.category === "Indian Markets"
    );

    const globalNews = news.filter(
        (article) =>
            article.category === "Global Markets"
    );

    const commodityNews = news.filter(
        (article) =>
            article.category === "Commodities"
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

    function NewsCard({ article }) {
        const publishedDate = article.published_at
            ? new Date(
                  article.published_at
              ).toLocaleDateString("en-IN", {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
              })
            : null;

        return (
            <a
                className="market-news-card"
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
            >
                <div className="market-news-card-top">
                    <span className="market-news-source">
                        {article.source || "Unknown source"}
                    </span>

                    <ExternalLink
                        size={14}
                        strokeWidth={2}
                    />
                </div>

                <h3>{article.title}</h3>

                {article.description && (
                    <p>
                        {article.description}
                    </p>
                )}

                <div className="market-news-card-footer">
                    <span>
                        {publishedDate || "Date unavailable"}
                    </span>
                </div>
            </a>
        );
    }

    function NewsSection({
        title,
        description,
        articles,
    }) {
        if (articles.length === 0) {
            return null;
        }

        return (
            <section className="market-news-section">
                <div className="market-section-heading">
                    <div>
                        <h2>{title}</h2>

                        <p>{description}</p>
                    </div>
                </div>

                <div className="market-news-grid">
                    {articles.map((article, index) => (
                        <NewsCard
                            key={`${article.url}-${index}`}
                            article={article}
                        />
                    ))}
                </div>
            </section>
        );
    }

    function EconomicEventCard({ event }) {
        const startDate = new Date(
            event.event_date
        ).toLocaleDateString("en-IN", {
            day: "2-digit",
            month: "short",
            year: "numeric",
        });

        const endDate = event.end_date
            ? new Date(
                  event.end_date
              ).toLocaleDateString("en-IN", {
                  day: "2-digit",
                  month: "short",
                  year: "numeric",
              })
            : null;

        const eventDate = endDate
            ? `${startDate} – ${endDate}`
            : startDate;

        return (
            <article className="market-event-card">
                <div className="market-event-card-top">
                    <span className="market-event-category">
                        {event.category}
                    </span>

                    <span
                        className={`market-event-status ${event.status}`}
                    >
                        {event.status}
                    </span>
                </div>

                <h3>{event.title}</h3>

                <div className="market-event-date">
                    {eventDate}
                </div>

                <p className="market-event-country">
                    {event.country}
                </p>

                {event.description && (
                    <p className="market-event-description">
                        {event.description}
                    </p>
                )}

                <div className="market-event-footer">
                    <span>
                        {event.source || "Unknown source"}
                    </span>

                    <a
                        href={event.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        aria-label={`Open source for ${event.title}`}
                    >
                        <ExternalLink
                            size={13}
                            strokeWidth={2}
                        />
                    </a>
                </div>
            </article>
        );
    }

    function EconomicEventsSection() {
        if (events.length === 0) {
            return null;
        }

        return (
            <section className="market-events-container">
                <div className="market-events-header">
                    <div>
                        <p className="eyebrow">
                            MACRO CALENDAR
                        </p>

                        <h2>
                            Economic & macro events.
                        </h2>

                        <p>
                            Scheduled events that can influence
                            markets, rates, currencies, and
                            commodities.
                        </p>
                    </div>
                </div>

                <div className="market-events-grid">
                    {events.map((event, index) => (
                        <EconomicEventCard
                            key={`${event.title}-${event.event_date}-${index}`}
                            event={event}
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

            <EconomicEventsSection />

            <section className="market-news-container">
                <div className="market-news-header">
                    <div>
                        <p className="eyebrow">
                            MARKET INTELLIGENCE
                        </p>

                        <h2>
                            Latest market news.
                        </h2>

                        <p>
                            Recent developments across Indian
                            markets, global markets, and
                            commodities.
                        </p>
                    </div>
                </div>

                <NewsSection
                    title="Indian Markets"
                    description="Recent developments in the Indian equity market."
                    articles={indianNews}
                />

                <NewsSection
                    title="Global Markets"
                    description="Major developments across international markets."
                    articles={globalNews}
                />

                <NewsSection
                    title="Commodities"
                    description="Recent developments in gold and silver markets."
                    articles={commodityNews}
                />
            </section>

            <div className="market-data-note">
                <span className="market-note-dot" />

                <span>
                    Market data is sourced from yfinance and
                    may be delayed. News and economic events
                    are retrieved from external sources.
                </span>
            </div>
        </>
    );
}

export default Market;