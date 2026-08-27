import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useCourse } from "../../hooks/course.actions";

import "../../styles/CourseList.css";

const CourseList = () => {
  const [page, setPage] = useState(1);
  const [ordering, setOrdering] = useState("-likes_count");
  const [userType, setUserType] = useState("");

  const filters = {
    ordering,
    author__user_type: userType || undefined,
  };

  const { course, loading, error, totalCount, loadCourse } = useCourse(null, filters);

  const pageSize = 25;
  const totalPages = Math.ceil(totalCount / pageSize);

  const handlePageChange = (newPage) => {
    setPage(newPage);
    loadCourse(newPage);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (loading) return <div className="state">Загрузка…</div>;
  if (error) return <div className="state error">Ошибка: {error}</div>;

  const courses = course?.results || [];

  if (courses.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">📚</div>
        <h3>Курсы не найдены</h3>
        <p>Попробуйте изменить фильтры</p>

        <button
          className="reset-btn"
          onClick={() => {
            setOrdering("-likes_count");
            setUserType("");
            setPage(1);
          }}
        >
          Сбросить фильтры
        </button>
      </div>
    );
  }

  return (
    <div className="courses-container">
      <div className="filters-header">
        <h2 className="courses-title">
          Все курсы <span className="count">({totalCount})</span>
        </h2>

        <div className="filters-controls">
          <div className="filter-item">
            <label className="filter-label">Сортировка</label>
            <select
              className="filter-select"
              value={ordering}
              onChange={(e) => {
                setOrdering(e.target.value);
                setPage(1);
              }}
            >
              <option value="-likes_count">🔥 Популярные</option>
              <option value="-students_count">👥 Больше студентов</option>
              <option value="-created">🆕 Новые</option>
              <option value="created">📜 Старые</option>
            </select>
          </div>

          <div className="filter-item">
            <label className="filter-label">Тип автора</label>
            <select
              className="filter-select"
              value={userType}
              onChange={(e) => {
                setUserType(e.target.value);
                setPage(1);
              }}
            >
              <option value="">Все авторы</option>
              <option value="school">Школа / Лицей</option>
              <option value="college">Колледж</option>
              <option value="university">Университет</option>
              <option value="pro_teacher">Преподаватель</option>
              <option value="organization">Организация</option>
            </select>
          </div>

          {(ordering !== "-likes_count" || userType) && (
            <button className="reset-filters-btn" onClick={() => {
              setOrdering("-likes_count");
              setUserType("");
              setPage(1);
            }}>
              Сбросить
            </button>
          )}
        </div>
      </div>

      <div className="courses-grid">
        {courses.map((c) => (
          <article key={c.public_id} className="course-card">
            <h3>
              <Link to={`/course/${c.public_id}`} className="course-title-link">
                {c.title || "Без названия"}
              </Link>
            </h3>

            {c.description && <p className="course-description">{c.description}</p>}

            <div className="course-meta">
              <span className="meta-item">❤️ {c.likes_count}</span>
              <span className="meta-item">👥 {c.students_count}</span>
              <Link to={`/user/${c.author.public_id}`} className="author-link">
                by {c.author.username}
              </Link>
            </div>
          </article>
        ))}
      </div>

      {/* Пагинация */}
      {totalPages > 1 && (
        <div className="pagination">
          <button onClick={() => handlePageChange(page - 1)} disabled={page === 1}>
            ← Назад
          </button>

          <span>Страница <strong>{page}</strong> из {totalPages}</span>

          <button onClick={() => handlePageChange(page + 1)} disabled={page === totalPages}>
            Вперед →
          </button>
        </div>
      )}
    </div>
  );
};

export default CourseList;