import UserMenu from "./UserMenu";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "../../styles/Header.css";

const Header = ({ toggleSidebar, sidebarOpen }) => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const query = searchParams.get("q") || "";
  const [search, setSearch] = useState(query);

  useEffect(() => {
    setSearch(query);
  }, [query]);

  const onSubmit = (e) => {
    e.preventDefault();
    if (!search.trim()) return;

    navigate(`/course/results?q=${encodeURIComponent(search)}`);
  };

  return (
    <header className="header">
      <div className="header-left">
        <button className="menu-toggle" onClick={toggleSidebar}>
          {sidebarOpen ? "✕" : "☰"}
        </button>
        <Link to="/" className="home-icon">🏠</Link>
      </div>

      <form className="search-box" onSubmit={onSubmit}>
        <input
          type="text"
          placeholder="Поиск курсов..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </form>

      <UserMenu />
    </header>
  );
};

export default Header;