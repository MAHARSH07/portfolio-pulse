import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { useEffect, useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import Notification from "./components/ui/Notification";
import "./App.css";
import StockDetail from "./components/portfolio/StockDetail";
import PlaceholderPage from "./pages/PlaceholderPage";
import Market from "./pages/Market";

function App() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);
  const [notification, setNotification] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState(null);

  async function loadPortfolio({ isRefresh = false } = {}) {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      setError("");

      const response = await fetch("http://127.0.0.1:8000/portfolio");

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

  const selectedHolding = portfolio?.holdings.find(
    (holding) => holding.symbol === selectedSymbol,
  );

  useEffect(() => {
    loadPortfolio();
  }, []);

  return (
    <BrowserRouter>
      <AppLayout>
        {loading && <div className="state-card">Loading portfolio...</div>}

        {!loading && error && (
          <div className="state-card error-state">{error}</div>
        )}

        {!loading && !error && portfolio && (
          <Routes>
            <Route path="/" element={<Navigate to="/overview" replace />} />

            <Route
              path="/overview"
              element={
                selectedHolding ? (
                  <StockDetail
                    holding={selectedHolding}
                    onBack={() => setSelectedSymbol(null)}
                  />
                ) : (
                  <Dashboard
                    portfolio={portfolio}
                    onRefresh={() =>
                      loadPortfolio({
                        isRefresh: true,
                      })
                    }
                    refreshing={refreshing}
                    lastUpdated={lastUpdated}
                    notification={notification}
                    onCloseNotification={() => setNotification(null)}
                    onSelectHolding={setSelectedSymbol}
                  />
                )
              }
            />

            <Route
              path="/portfolio"
              element={
                <PlaceholderPage
                  title="Portfolio"
                  description="Explore your holdings, positions, transactions, and portfolio history."
                />
              }
            />

            <Route path="/market" element={<Market />} />

            <Route
              path="/news"
              element={
                <PlaceholderPage
                  title="News"
                  description="See market and company news filtered around your portfolio."
                />
              }
            />

            <Route
              path="/alerts"
              element={
                <PlaceholderPage
                  title="Alerts"
                  description="Important portfolio events and market signals will appear here."
                />
              }
            />

            <Route
              path="/assistant"
              element={
                <PlaceholderPage
                  title="AI Assistant"
                  description="Your portfolio-aware intelligence assistant will live here."
                />
              }
            />

            <Route
              path="/settings"
              element={
                <PlaceholderPage
                  title="Settings"
                  description="Manage your PortfolioPulse account, broker connection, and preferences."
                />
              }
            />

            <Route path="*" element={<Navigate to="/overview" replace />} />
          </Routes>
        )}
      </AppLayout>
    </BrowserRouter>
  );
}

export default App;
