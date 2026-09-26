const currencyFormatter = new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 2,
});

function HoldingsTable({ holdings }) {
  return (
    <div className="holdings-card">
      <div className="holdings-header">
        <span>Stock</span>
        <span>Quantity</span>
        <span>Avg. price</span>
        <span>Current value</span>
        <span>P&L</span>
      </div>

      <div className="holdings-body">
        {holdings.map((holding) => {
          const hasMarketPrice =
            Number(holding.current_price) > 0;

          return (
            <div
              className="holding-row"
              key={holding.symbol}
            >
              <div className="stock-cell">
                <div className="stock-avatar">
                  {holding.symbol.charAt(0)}
                </div>

                <div className="stock-details">
                  <strong>{holding.symbol}</strong>

                  <span>
                    {holding.company_name ||
                      "Market data pending"}
                  </span>
                </div>
              </div>

              <span className="table-number">
                {holding.quantity}
              </span>

              <span className="table-number">
                {currencyFormatter.format(
                  holding.average_price
                )}
              </span>

              <strong className="table-number">
                {hasMarketPrice
                  ? currencyFormatter.format(
                      holding.current_value
                    )
                  : "—"}
              </strong>

              <span
                className={`table-number ${
                  hasMarketPrice
                    ? holding.pnl >= 0
                      ? "value-positive"
                      : "value-negative"
                    : ""
                }`}
              >
                {hasMarketPrice
                  ? `${holding.pnl >= 0 ? "+" : ""}${currencyFormatter.format(
                      holding.pnl
                    )}`
                  : "—"}
              </span>
            </div>
          );
        })}
      </div>

      <div className="holdings-footer">
        <span>
          Showing {holdings.length}{" "}
          {holdings.length === 1 ? "holding" : "holdings"}
        </span>

        <span>
          Invested value:{" "}
          {currencyFormatter.format(
            holdings.reduce(
              (total, holding) =>
                total +
                Number(holding.quantity) *
                  Number(holding.average_price),
              0
            )
          )}
        </span>
      </div>
    </div>
  );
}

export default HoldingsTable;