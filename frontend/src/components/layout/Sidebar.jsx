import {
  LayoutDashboard,
  BriefcaseBusiness,
  Newspaper,
  Bell,
  Bot,
  Settings,
} from "lucide-react";

const navigationItems = [
  {
    label: "Overview",
    icon: LayoutDashboard,
    active: true,
  },
  {
    label: "Portfolio",
    icon: BriefcaseBusiness,
  },
  {
    label: "Market",
    icon: Newspaper,
  },
  {
    label: "News",
    icon: Newspaper,
  },
  {
    label: "Alerts",
    icon: Bell,
  },
  {
    label: "AI Assistant",
    icon: Bot,
  },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark">P</div>

        <div>
          <div className="brand-name">PortfolioPulse</div>
          <div className="brand-subtitle">Market intelligence</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">WORKSPACE</div>

        {navigationItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className={`nav-item ${item.active ? "active" : ""}`}
            >
              <Icon size={18} strokeWidth={1.8} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-bottom">
        <button className="nav-item">
          <Settings size={18} strokeWidth={1.8} />
          <span>Settings</span>
        </button>

        <div className="sidebar-status">
          <div className="status-dot" />
          <div>
            <div className="status-title">Groww connected</div>
            <div className="status-subtitle">Sync available</div>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;