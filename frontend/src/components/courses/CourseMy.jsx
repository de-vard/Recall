import React from "react";
import { Link } from "react-router-dom";
import "../../styles/CourseList.css";
import { useCourse } from "../../hooks/course.actions";

const CourseMy = () => {
  const { myCourses, loading, error } = useCourse();

  if (loading) return <div className="state">Загрузка…</div>;
  if (error) return <div className="state error">Ошибка: {error}</div>;

  // Если бэкенд возвращает просто массив — используем его
  // Если возвращает { results: [...] } — берём results
  const courses = Array.isArray(myCourses) ? myCourses : myCourses?.results || [];

  if (courses.length === 0) {
    return <div className="state">У вас пока нет курсов</div>;
  }

  return (
    <div className="courses-container">
      <h2 className="courses-title">
        Курсы, на которые подписан или созданные мной
      </h2>

      <div className="courses-grid">
        {courses.map((c) => (
          <article key={c.public_id} className="course-card">
            <h3>
              <Link to={`/course/${c.public_id}`} className="course-title-link">
                {c.title || "Без названия"}
              </Link>
            </h3>

            {c.description && (
              <p className="course-description">{c.description}</p>
            )}

            <div className="course-meta">
              <span className="meta-item">❤️ {c.likes_count}</span>
              <span className="meta-item">👥 {c.students_count}</span>
              <Link
                to={`/user/${c.author.public_id}`}
                className="author-link"
              >
                by {c.author.username}
              </Link>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
};

export default CourseMy;