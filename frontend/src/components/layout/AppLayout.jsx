import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

function AppLayout({ children }) {
  return (
    <div className="app-shell">
      <Sidebar />

      <div className="app-main">
        <TopBar />

        <main className="page-content">
          {children}
        </main>
      </div>
    </div>
  );
}

export default AppLayout;