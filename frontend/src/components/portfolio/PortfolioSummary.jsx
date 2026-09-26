import {
  BriefcaseBusiness,
  CircleDollarSign,
  TrendingUp,
} from "lucide-react";
import MetricCard from "../ui/MetricCard";

const currencyFormatter = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 2,
});

function formatCurrency(value) {
  return currencyFormatter.format(value);
}

function PortfolioSummary({ portfolio }) {
  const holdingsCount = portfolio.holdings.length;

  const hasMarketData = portfolio.holdings.some(
    (holding) => Number(holding.current_price) > 0
  );

  const investedValue = Number(portfolio.total_invested) || 0;
  const currentValue = Number(portfolio.total_current_value) || 0;
  const pnl = Number(portfolio.total_pnl) || 0;
  const pnlPercentage =
    Number(portfolio.total_pnl_percentage) || 0;

  return (
    <section className="metrics-grid">
      <MetricCard
        label="Invested"
        value={formatCurrency(investedValue)}
        meta={`${holdingsCount} ${
          holdingsCount === 1 ? "holding" : "holdings"
        }`}
        secondary="Total capital invested"
        icon={BriefcaseBusiness}
        status="neutral"
      />

      <MetricCard
        label="Current value"
        value={hasMarketData ? formatCurrency(currentValue) : "—"}
        meta={
          hasMarketData
            ? "Based on live prices"
            : "Market prices unavailable"
        }
        secondary={
          hasMarketData
            ? "Current portfolio valuation"
            : "Waiting for market data"
        }
        icon={CircleDollarSign}
        status={hasMarketData ? "neutral" : "pending"}
      />

      <MetricCard
        label="Unrealized P&L"
        value={
          hasMarketData
            ? `${pnl >= 0 ? "+" : ""}${formatCurrency(pnl)}`
            : "—"
        }
        meta={
          hasMarketData
            ? `${pnlPercentage >= 0 ? "+" : ""}${pnlPercentage.toFixed(2)}%`
            : "Awaiting market prices"
        }
        secondary={
          hasMarketData
            ? "Current unrealized return"
            : "P&L will appear after price sync"
        }
        icon={TrendingUp}
        status={
          !hasMarketData
            ? "pending"
            : pnl >= 0
              ? "positive"
              : "negative"
        }
      />
    </section>
  );
}

export default PortfolioSummary;