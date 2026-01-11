import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useCourse } from "../../hooks/course.actions";
import "../../styles/CourseEdit.css";

const CourseEdit = () => {
  const [error, setError] = useState(null);
  const { public_id } = useParams();
  const navigate = useNavigate();
  const { course, editCourse } = useCourse(public_id);

  const [form, setForm] = useState({
    title: "",
    description: "",
    is_public: false,
  });

  useEffect(() => {
    if (course) {
      setForm({
        title: course.title || "",
        description: course.description || "",
        is_public: Boolean(course.is_public),
      });
    }
  }, [course]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await editCourse(form);
      navigate(`/course/${public_id}`);
    } catch (err) {
      const data = err.response?.data;
      setError(
        typeof data === "string"
          ? data
          : data
            ? Object.values(data)[0][0]
            : "Ошибка сервера",
      );
    }
  };

  return (
    <div className="form-page">
      <form className="form-card" onSubmit={handleSubmit}>
        <h2>Редактирование курса</h2>

        {error && <p className="form-error">{error}</p>}

        <label>
          Название курса
          <input
            name="title"
            value={form.title}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Описание
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            rows={6}
            placeholder="Подробное описание курса"
          />
        </label>

        <label className="checkbox">
          <input
            type="checkbox"
            name="is_public"
            checked={form.is_public}
            onChange={handleChange}
          />
          Публичный курс
        </label>

        <button type="submit">Сохранить</button>
      </form>
    </div>
  );
};

export default CourseEdit;
