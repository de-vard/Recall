import React from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { useCourse } from "../../hooks/course.actions";
import CourseActionButtons from "./CourseActionButtons";
import moduleIcon from "../../assets/lesson-1.png";
import subscribeIcon from "../../assets/subscribe.png";
import unsubscribeIcon from "../../assets/unfollow.png";
import likeIcon from "../../assets/like.png";
import dislikeIcon from "../../assets/dislike.png";
import "../../styles/CourseDetail.css";

const CourseDetail = () => {
  const { public_id } = useParams();
  const navigate = useNavigate();
  const { course, loading, error, toggleReaction, toggleSubscription } =
    useCourse(public_id);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;
  if (!course) return <div>Нет данных</div>;

  const handleGoBack = () => {
    course.folder_title === "home"
      ? navigate("/")
      : navigate(`/folder/${course.folder}`);
  };

  return (
    <div className="course-page">
      <div className="course-card">
        <h2>Наименование курса: {course.title}</h2>
         <div className="action-button"><CourseActionButtons public_id={course.public_id} /></div>
        <p className="desc">{course.description}</p>

        <div className="meta">
          <span>👤 {course.author}</span>
          <span>👥 {course.students_count}</span>
          <span>❤️ {course.likes_count}</span>
        </div>

       

        <div className="course-actions">
          <button
            className={`action-btn ${course.is_liked ? "active" : ""}`}
            onClick={toggleReaction}
          >
            <img src={course.is_liked ? dislikeIcon : likeIcon} alt="" />
            {course.is_liked ? "Убрать лайк" : "Лайк"}
          </button>

          <button
            className={`action-btn ${course.is_subscribed ? "active" : ""}`}
            onClick={toggleSubscription}
          >
            <img
              src={course.is_subscribed ? unsubscribeIcon : subscribeIcon}
              alt=""
            />
            {course.is_subscribed ? "Отписаться" : "Подписаться"}
          </button>
        </div>
      </div>

      <div className="lessons">
        <h3>Уроки</h3>

        {course.lessons?.length === 0 && (
          <p className="empty">Уроков пока нет</p>
        )}

        <div className="lesson-grid">
          {course.lessons?.map((lesson) => (
            <Link
              key={lesson.public_id}
              to={`/module/${lesson.public_id}`}
              className="lesson-card"
            >
              <img src={moduleIcon} alt="Урок" />
              <span>{lesson.title}</span>
            </Link>
          ))}
        </div>
      </div>
      <br />
      <button className="back-button" onClick={handleGoBack}>
        Назад
      </button>
    </div>
  );
};

export default CourseDetail;
