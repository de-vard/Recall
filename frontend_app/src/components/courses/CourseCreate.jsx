import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useCourse } from "../../hooks/course.actions";
import "../../styles/CourseCreate.css";

const CourseCreate = () => {
  const { public_id } = useParams();
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    title: "",
    description: "",
    folder: public_id,
    is_public: false,
  });

  const navigate = useNavigate();
  const { createCourse } = useCourse();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createCourse(form);
      navigate(`/folder/${public_id}`);
    } catch (err) {
      if (err.response?.data) {
        if (typeof err.response.data === "string") {
          setError(err.response.data);
        } else {
          const errors = Object.values(err.response.data);
          setError(errors.flat().join(", "));
        }
      } else if (err.message) {
        setError(err.message);
      } else {
        setError("Произошла ошибка при создании курса");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="course-create-container">
      <h1 className="course-create-title">Создание курса</h1>
      
      <form className="course-create-form" onSubmit={handleSubmit}>
        {error && (
          <div className="course-create-error">
            ⚠️ {error}
          </div>
        )}

        <div className="course-create-group">
          <label className="course-create-label">Название курса*</label>
          <input
            className="course-create-input"
            name="title"
            type="text"
            value={form.title}
            onChange={handleChange}
            required
            placeholder="Введите название курса"
            maxLength={100}
          />
        </div>

        <div className="course-create-group">
          <label className="course-create-label">Описание курса</label>
          <textarea
            className="course-create-input"
            name="description"
            value={form.description}
            onChange={handleChange}
            placeholder="Добавьте описание курса (необязательно)"
            rows={4}
            maxLength={500}
          />
        </div>

        <div className="course-create-group">
          <label className="course-create-checkbox-group">
            <input
              className="course-create-checkbox-input"
              name="is_public"
              type="checkbox"
              checked={form.is_public}
              onChange={handleChange}
            />
            <span>Публичный курс (доступен всем пользователям)</span>
          </label>
        </div>

        <button 
          className="course-create-submit" 
          type="submit"
          disabled={loading}
        >
          {loading ? "Создание..." : "Создать курс"}
        </button>
      </form>
    </div>
  );
};

export default CourseCreate;