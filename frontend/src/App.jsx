import { useEffect, useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import Notification from "./components/ui/Notification";
import "./App.css";

function App() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);
  const [notification, setNotification] = useState(null);

  async function loadPortfolio({ isRefresh = false } = {}) {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      setError("");

      const response = await fetch(
        "http://127.0.0.1:8000/portfolio"
      );

      if (!response.ok) {
        throw new Error("Unable to load portfolio.");
      }

      const data = await response.json();

      setPortfolio(data);
      setLastUpdated(new Date());

      if (isRefresh) {
        setNotification({
          type: "success",
          message: "Portfolio refreshed successfully.",
        });
      }
    } catch (err) {
      if (isRefresh) {
        setNotification({
          type: "error",
          message: "Unable to refresh portfolio. Please try again.",
        });
      } else {
        setError(err.message);
      }
    } finally {
      if (isRefresh) {
        setRefreshing(false);
      } else {
        setLoading(false);
      }
    }
  }

  useEffect(() => {
    loadPortfolio();
  }, []);

  return (
    <AppLayout>
      {loading && <div className="state-card">Loading portfolio...</div>}

      {!loading && error && (
        <div className="state-card error-state">
          {error}
        </div>
      )}

      {!loading && !error && portfolio && (
        <Dashboard
          portfolio={portfolio}
          onRefresh={() => loadPortfolio({ isRefresh: true })}
          refreshing={refreshing}
          lastUpdated={lastUpdated}
          notification={notification}
          onCloseNotification={() => setNotification(null)}
        />
      )}
    </AppLayout>
  );
}

export default App;