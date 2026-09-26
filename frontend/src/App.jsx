import { useEffect, useState } from "react";
import TransactionList from "./components/TransactionList";

function App() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/portfolio")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch portfolio");
        }

        return response.json();
      })
      .then((data) => {
        setPortfolio(data);
      })
      .catch(() => {
        setError("Unable to load portfolio");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading portfolio...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <div>
      <h1>PortfolioPulse</h1>

      <p>Your investment portfolio</p>

      <h2>
        ₹{portfolio.total_current_value.toFixed(2)}
      </h2>

      <p>
        P&L: ₹{portfolio.total_pnl.toFixed(2)} (
        {portfolio.total_pnl_percentage.toFixed(2)}%
        )
      </p>

      <h2>Holdings</h2>

      <table>
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Company</th>
            <th>Quantity</th>
            <th>Average Price</th>
            <th>Current Price</th>
            <th>Current Value</th>
            <th>P&L</th>
          </tr>
        </thead>

        <tbody>
          {portfolio.holdings.map((holding) => (
            <tr key={holding.symbol}>
              <td>{holding.symbol}</td>
              <td>{holding.company_name}</td>
              <td>{holding.quantity}</td>
              <td>₹{holding.average_price.toFixed(2)}</td>
              <td>₹{holding.current_price.toFixed(2)}</td>
              <td>₹{holding.current_value.toFixed(2)}</td>
              <td>
                ₹{holding.pnl.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <TransactionList />
    </div>
  );
}

export default App;