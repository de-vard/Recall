import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useModule } from "../../hooks/module.actions";
import "../../styles/CourseDelete.css";

const ModuleDelete = () => {
  const [error, setError] = useState(null);
  const { public_id } = useParams();
  const navigate = useNavigate();
  const { module, deleteModule } = useModule(public_id);

  const handleCancel = () => {
    //При отмене удаления возвращаемся обратно
    navigate(-1); // возвращаемся назад
  };

  const handleDelete = async () => {
    try {
      await deleteModule();
      navigate(`/course/${module.course.public_id}`);
    } catch (err) {
      if (err.response?.data) {
        // DRF обычно возвращает объект
        if (typeof err.response.data === "string") {
          setError(err.response.data);
        } else {
          const firstError = Object.values(err.response.data)[0];
          setError(Array.isArray(firstError) ? firstError[0] : firstError);
        }
      } else {
        setError("Ошибка на стороне сервера");
      }
    }
  };

  return (
    <div className="course-delete-page">
      <div className="course-delete-card">
        <h1>Вы действительно хотите удалить модуль?</h1>
        {error && <p className="error">{error}</p>}
        <div className="course-delete-buttons">
          <button className="delete" onClick={handleDelete}>Да</button>
          <button className="cancel" onClick={handleCancel}>Нет</button>
        </div>
      </div>
    </div>
  );
};

export default ModuleDelete;
