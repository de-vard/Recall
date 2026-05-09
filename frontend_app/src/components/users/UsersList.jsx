import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useUser } from "../../hooks/useUser";

import "../../styles/UsersList.css";

const UsersList = () => {
  const [page, setPage] = useState(1);
  const [userType, setUserType] = useState("");

  const filters = {
    user_type: userType || undefined,
  };

  const { users, loading, error, totalCount, loadUsers } = useUser(null, filters);

  const pageSize = 25;
  const totalPages = Math.ceil(totalCount / pageSize);

  const handlePageChange = (newPage) => {
    setPage(newPage);
    loadUsers(newPage);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (loading) return <div className="state">Загрузка пользователей…</div>;
  if (error) return <div className="state error">Ошибка: {error}</div>;

  if (totalCount === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">👥</div>
        <h3>Пользователи не найдены</h3>
        <p>Попробуйте изменить фильтр</p>
        <button className="reset-btn" onClick={() => { setUserType(""); setPage(1); }}>
          Показать всех
        </button>
      </div>
    );
  }

  return (
    <div className="users-container">
      <div className="filters-header">
        <h2 className="users-title">
          Все пользователи <span className="count">({totalCount})</span>
        </h2>

        <div className="filters-controls">
          <div className="filter-item">
            <label className="filter-label">Тип пользователя</label>
            <select
              className="filter-select"
              value={userType}
              onChange={(e) => {
                setUserType(e.target.value);
                setPage(1);
              }}
            >
              <option value="">Все пользователи</option>
              <option value="school">🏫 Школа / Лицей</option>
              <option value="college">📚 Колледж / Техникум</option>
              <option value="university">🎓 Университет</option>
              <option value="pro_teacher">👨‍🏫 Преподаватель</option>
              <option value="organization">🏢 Организация</option>
              <option value="simple_user">👤 Обычный пользователь</option>
            </select>
          </div>

          {userType && (
            <button
              className="reset-filters-btn"
              onClick={() => {
                setUserType("");
                setPage(1);
              }}
            >
              Сбросить
            </button>
          )}
        </div>
      </div>

      <div className="users-grid">
        {users.map((u) => (
          <article key={u.public_id} className="user-card">
            <Link to={`/user/${u.public_id}`} className="avatar-container">
              {u.avatar ? (
                <img src={u.avatar} alt={u.username} className="user-avatar" />
              ) : (
                <div className="avatar-placeholder">
                  {u.username?.[0]?.toUpperCase() || "?"}
                </div>
              )}
              {/* Онлайн индикатор (если есть данные) */}
              {u.is_online && <div className="online-dot" />}
            </Link>

            <div className="user-info">
              <h3 className="username">
                <Link to={`/user/${u.public_id}`}>{u.username}</Link>
              </h3>

              {u.user_type && (
                <span className="user-type">
                  {u.user_type === "pro_teacher" 
                    ? "👨‍🏫 Преподаватель" 
                    : u.user_type === "organization" 
                    ? "🏢 Организация" 
                    : u.user_type === "school" 
                    ? "🏫 Школа" 
                    : "👤 Пользователь"}
                </span>
              )}

            </div>
          </article>
        ))}
      </div>

      {/* Улучшенная пагинация */}
      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => handlePageChange(page - 1)}
            disabled={page === 1}
            className="page-btn prev"
          >
            ← Назад
          </button>

          <div className="page-info">
            Страница <strong>{page}</strong> из {totalPages}
          </div>

          <button
            onClick={() => handlePageChange(page + 1)}
            disabled={page === totalPages}
            className="page-btn next"
          >
            Вперед →
          </button>
        </div>
      )}
    </div>
  );
};

export default UsersList;