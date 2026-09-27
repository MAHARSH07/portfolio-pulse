import {
  LayoutDashboard,
  BriefcaseBusiness,
  Newspaper,
  Bell,
  Bot,
  Settings,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navigationItems = [
  {
    label: "Overview",
    icon: LayoutDashboard,
    path: "/overview",
  },
  {
    label: "Portfolio",
    icon: BriefcaseBusiness,
    path: "/portfolio",
  },
  {
    label: "Market",
    icon: Newspaper,
    path: "/market",
  },
  {
    label: "News",
    icon: Newspaper,
    path: "/news",
  },
  {
    label: "Alerts",
    icon: Bell,
    path: "/alerts",
  },
  {
    label: "AI Assistant",
    icon: Bot,
    path: "/assistant",
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
            <NavLink
              key={item.label}
              to={item.path}
              end={item.path === "/overview"}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              <Icon size={18} strokeWidth={1.8} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-bottom">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `nav-item ${isActive ? "active" : ""}`
          }
        >
          <Settings size={18} strokeWidth={1.8} />
          <span>Settings</span>
        </NavLink>

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