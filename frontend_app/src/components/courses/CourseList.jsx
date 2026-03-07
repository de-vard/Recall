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
    author__user_type: userType || undefined, // если "", то не отправляем
    page,                                     // ← важно!
    page_size: 12,                            // согласуй с бэкендом
  };


  const { course, loading, error } = useCourse(null, filters);
  const [currentPage, setCurrentPage] = useState(1);

  // Предполагаем, что по 6 курсов на страницу (можно изменить)
  const itemsPerPage = 6;

  if (loading) return <div className="state">Загрузка…</div>;
  if (error) return <div className="state error">Ошибка: {error}</div>;
  if (!course?.results?.length) {
  return (
    <div className="empty-state">
      <div className="empty-icon">📚</div>
      <h3>Курсы не найдены</h3>
      <p>Попробуйте изменить фильтры или сбросить их</p>

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

  const courses = course.results;

  // Вычисляем данные для текущей страницы
  const indexOfLast = currentPage * itemsPerPage;
  const indexOfFirst = indexOfLast - itemsPerPage;
  const currentCourses = courses.slice(indexOfFirst, indexOfLast);

  // Общее количество страниц
  const totalPages = Math.ceil(courses.length / itemsPerPage);



  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="courses-container">
      <div className="filters-header">
  <h2 className="courses-title">Все курсы</h2>

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
        <option value="-author__username">Автор Я→А</option>
        <option value="author__username">Автор А→Я</option>
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
        <option value="school">Школа / Лицей / Гимназия</option>
        <option value="college">Колледж / Техникум</option>
        <option value="university">Университет / Институт</option>
        <option value="other_edu">Другое образовательное учреждение</option>
        <option value="pro_teacher">Профессиональный преподаватель</option>
        <option value="organization">Организация / Компания</option>
        <option value="simple_user">Простой пользователь</option>
      </select>
    </div>

    {(ordering !== "-likes_count" || userType) && (
      <button
        className="reset-filters-btn"
        onClick={() => {
          setOrdering("-likes_count");
          setUserType("");
          setPage(1);
        }}
      >
        Сбросить
      </button>
    )}

  </div>
</div>

      <div className="courses-grid">
        {currentCourses.map((c) => (
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
          <button
            onClick={() => handlePageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className="page-btn"
          >
            ← Назад
          </button>

          {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
            <button
              key={page}
              onClick={() => handlePageChange(page)}
              className={`page-btn ${currentPage === page ? "active" : ""}`}
            >
              {page}
            </button>
          ))}

          <button
            onClick={() => handlePageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="page-btn"
          >
            Вперед →
          </button>
        </div>
      )}
    </div>
  );
};

export default CourseList;