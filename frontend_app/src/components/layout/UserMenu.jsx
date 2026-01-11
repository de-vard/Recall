import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useUserActions, getUser } from "../../hooks/user.actions";
import "../../styles/UserMenu.css";

const UserMenu = () => {
  const { logout } = useUserActions();
  const [open, setOpen] = useState(false);
  const menuRef = useRef(null);
  const user = getUser();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
  };
  
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="user-menu" ref={menuRef}>
      <div className="user-trigger" onClick={() => setOpen(!open)}>
        <span className="user-icon">👤</span>
        <span className="user-name">{user.username}***</span>
      </div>

      {open && (
        <div className="user-dropdown">
          <button onClick={() => navigate(`/coming-soon`)}>✏️ Редактировать</button>
          <button className="danger" onClick={handleLogout}>
            🚪 Выйти
          </button>
        </div>
      )}
    </div>
  );
};

export default UserMenu;
