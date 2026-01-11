import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useFolder } from "../../hooks/folder.actions";
import "../../styles/FolderForm.css";

const FolderCreate = () => {
  const [error, setError] = useState(null);
  const { public_id } = useParams();
  const [form, setForm] = useState({
    title: "",
    parent_public_id: public_id,
  });

  const { createFolder } = useFolder();
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createFolder(form);
      navigate(`/folder/${public_id}`);
    } catch (err) {
      const data = err.response?.data;
      let message = "Ошибка сервера";

      if (typeof data === "string") message = data;
      else if (data) {
        const first = Object.values(data)[0];
        message = Array.isArray(first) ? first.join(" ") : String(first);
      }

      setError(message);
    }
  };

  return (
    <section className="folder-form-page">
      <form className="folder-form" onSubmit={handleSubmit}>
        <h1>Создание папки</h1>

        {error && <p className="error">{error}</p>}

        <label>
          Наименование папки
          <input
            name="title"
            type="text"
            placeholder="Название папки"
            value={form.title}
            onChange={handleChange}
            required
          />
        </label>

        <button type="submit">Создать</button>
      </form>
    </section>
  );
};

export default FolderCreate;
