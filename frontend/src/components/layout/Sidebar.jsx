import "../../styles/Sidebar.css";
import { useNavigate } from "react-router-dom";

const Sidebar = ({ isOpen, toggle }) => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    // Закрываем Sidebar при клике на кнопку
    toggle();
    // Здесь можно добавить дополнительную логику
  };

  return (
    <aside className={`sidebar ${isOpen ? "open" : ""}`}>
      <button className="sidebar-btn" onClick={() => navigate(`/`)}>
        📁 Мои папки
      </button>
      <button className="sidebar-btn" onClick={() => navigate(`/course/my`)}>
        📘 Мои курсы 
      </button>
      <button className="sidebar-btn" onClick={() => navigate(`course/`)}>
        🔥 Популярные курсы
      </button>
      <button className="sidebar-btn" onClick={() => navigate(`users/`)}>
        🙍🏻‍♂️ Пользователи 
      </button>
    </aside>
  );
};

export default Sidebar;
