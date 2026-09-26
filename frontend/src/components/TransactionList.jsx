import { useEffect, useState } from "react";

function TransactionList() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/transactions")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch transactions");
        }

        return response.json();
      })
      .then((data) => {
        setTransactions(data);
      })
      .catch(() => {
        setError("Unable to load transactions");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading transactions...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  return (
    <section>
      <h2>Transaction History</h2>

      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Symbol</th>
            <th>Type</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Total</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>
                {new Date(
                  transaction.transaction_date
                ).toLocaleDateString()}
              </td>

              <td>{transaction.symbol}</td>

              <td>{transaction.transaction_type}</td>

              <td>{transaction.quantity}</td>

              <td>
                ₹{transaction.price.toFixed(2)}
              </td>

              <td>
                ₹{transaction.total_amount.toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

export default TransactionList;