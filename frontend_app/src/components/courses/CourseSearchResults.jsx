import { Link, useLocation } from "react-router-dom";
import "../../styles/CourseList.css";

const CourseSearchResults = ({ results = [], loading }) => {
  const location = useLocation();

  if (loading) {
    return <div className="state">Поиск…</div>;
  }

  if (!results.length) {
    return <div className="state">Ничего не найдено</div>;
  }

  return (
    <div className="courses-grid">
      {results.map((c) => (
        <article key={c.public_id} className="course-card">
          <h3>
            <Link
              to={`/course/${c.public_id}`}
              state={{ from: location }}
              className="course-title-link"
            >
              {c.title || "Без названия"}
            </Link>
          </h3>

          {c.description && (
            <p className="course-description">{c.description}</p>
          )}

          <div className="course-meta">
            {c.likes_count != null && (
              <span className="meta-item">❤️ {c.likes_count}</span>
            )}
            {c.students_count != null && (
              <span className="meta-item">👥 {c.students_count}</span>
            )}
          </div>
        </article>
      ))}
    </div>
  );
};

export default CourseSearchResults;