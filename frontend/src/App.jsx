import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
  useLocation,
} from "react-router-dom";
import { useEffect, useState } from "react";
import AppLayout from "./components/layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import Notification from "./components/ui/Notification";
import "./App.css";
import StockDetail from "./components/portfolio/StockDetail";
import PlaceholderPage from "./pages/PlaceholderPage";
import Market from "./pages/Market";
import Assistant from "./pages/Assistant";
import Portfolio from "./pages/Portfolio";

function AppContent() {
  const location = useLocation();

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

      // Sync the latest holdings from Groww when Refresh is clicked.
      if (isRefresh) {
        const syncResponse = await fetch(
          "http://127.0.0.1:8000/sync/portfolio",
          { method: "POST" },
        );

        if (!syncResponse.ok) {
          throw new Error("Unable to synchronize holdings from Groww.");
        }
      }

      // Load the latest portfolio after synchronization.
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
          message: "Portfolio synchronized and refreshed successfully.",
        });
      }
    } catch (err) {
      if (isRefresh) {
        setNotification({
          type: "error",
          message:
            err.message || "Unable to refresh portfolio. Please try again.",
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

  const isOverview = location.pathname === "/overview";
  const showGlobalLoading = loading && isOverview;
  const showGlobalError = !loading && error && isOverview;

  return (
    <AppLayout>
      {showGlobalLoading && (
        <div className="state-card">Loading overview...</div>
      )}

      {showGlobalError && <div className="state-card error-state">{error}</div>}

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
                  onRefresh={() => loadPortfolio({ isRefresh: true })}
                  refreshing={refreshing}
                  lastUpdated={lastUpdated}
                  notification={notification}
                  onCloseNotification={() => setNotification(null)}
                  onSelectHolding={setSelectedSymbol}
                />
              )
            }
          />

          <Route path="/portfolio" element={<Portfolio />} />
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

          <Route path="/assistant" element={<Assistant />} />

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
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
