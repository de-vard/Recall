import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useCourse } from "../../hooks/course.actions";
import "../../styles/CourseList.css";

const CourseList = () => {
  const { course, loading, error } = useCourse();
  const [currentPage, setCurrentPage] = useState(1);

  // Предполагаем, что по 6 курсов на страницу (можно изменить)
  const itemsPerPage = 6;

  if (loading) return <div className="state">Загрузка…</div>;
  if (error) return <div className="state error">Ошибка: {error}</div>;
  if (!course?.results?.length) return <div className="state">Нет курсов</div>;

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
      <h2 className="courses-title">Все курсы</h2>

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