import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useFolder } from "../../hooks/folder.actions";
import "../../styles/FolderForm.css";

const FolderEdit = () => {
  const [form, setForm] = useState({ title: "" });
  const [error, setError] = useState(null);
  const { public_id } = useParams();
  const navigate = useNavigate();

  const { folder, editFolder } = useFolder(public_id);

  useEffect(() => {
    if (folder) setForm({ title: folder.title || "" });
  }, [folder]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await editFolder(form);
      navigate(`/folder/${public_id}`);
    } catch (err) {
      const data = err.response?.data;
      const msg =
        typeof data === "string"
          ? data
          : data
          ? Object.values(data)
          : "Ошибка сервера";
      setError(msg);
    }
  };

  return (
    <section className="folder-form-page">
      <form className="folder-form" onSubmit={handleSubmit}>
        <h1>Редактирование папки</h1>

        {error && <p className="form-error">{error}</p>}

        <label>
          Наименование папки
          <input
            name="title"
            type="text"
            placeholder="Глаголы"
            value={form.title}
            onChange={handleChange}
            required
          />
        </label>

        <button type="submit">Сохранить</button>
      </form>
    </section>
  );
};

export default FolderEdit;
