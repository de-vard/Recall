import UserMenu from "./UserMenu";
import { Link } from "react-router-dom";

const Header = ({ toggleSidebar, sidebarOpen }) => {
  return (
    <header className="header">
      <div className="header-left">
        <button className="menu-toggle" onClick={toggleSidebar}>
          {sidebarOpen ? "✕" : "☰"}
        </button>
        <Link to="/" className="home-icon" title="На главную">
          🏠
        </Link>
      </div>

      <div className="search-box">
        <input type="text" placeholder="Поиск пока не работает(..." />
      </div>

      <UserMenu />
    </header>
  );
};

export default Header;
