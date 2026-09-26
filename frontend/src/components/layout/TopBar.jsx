import { Bell, Search } from "lucide-react";

function TopBar() {
  return (
    <header className="topbar">
      <div className="search-box">
        <Search size={17} />
        <input
          type="text"
          placeholder="Search stocks, news, companies..."
        />
        <span className="search-shortcut">⌘ K</span>
      </div>

      <div className="topbar-actions">
        <div className="market-status">
          <span className="market-status-dot" />
          <span>Market data</span>
        </div>

        <button className="icon-button">
          <Bell size={18} />
        </button>

        <div className="profile">
          <div className="profile-avatar">M</div>

          <div className="profile-info">
            <span className="profile-name">Maharsh</span>
            <span className="profile-role">Investor</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default TopBar;