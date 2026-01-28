import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUserActions } from "../../hooks/user.actions";
import SocialLoginButtons from "./SocialLoginButtons";
import EmailVerificationNotice from "../auth/EmailVerificationNotice";
import "../../styles/Registration.css"; // Добавляем импорт стилей

const Registration = () => {
  const navigate = useNavigate();
  const register = useUserActions().register;
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [emailForVerify, setEmailForVerify] = useState(null);

  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  setError(null);
  setLoading(true);

  try {
    const formData = new FormData();
    formData.append("username", form.username);
    formData.append("email", form.email);
    formData.append("password", form.password);

    const response = await register(formData);

    // показываем экран подтверждения
    setEmailForVerify(form.email);
  } catch (err) {
    // err.response.data содержит ошибки от сервера
    if (err.response && err.response.data) {
      const errors = err.response.data;
      // Формируем текст ошибки для пользователя
      const messages = [];
      if (errors.email) messages.push(`Email: ${errors.email.join(" ")}`);
      if (errors.username) messages.push(`Логин: ${errors.username.join(" ")}`);
      if (errors.password) messages.push(`Пароль: ${errors.password.join(" ")}`);
      setError(messages.join(" | "));
    } else {
      setError("Ошибка регистрации");
    }
  } finally {
    setLoading(false);
  }
};
  if (emailForVerify) {
    return <EmailVerificationNotice email={emailForVerify} />;
  }

  return (
    <section className="registration-section">
      <h1>Регистрация</h1>

      <form onSubmit={handleSubmit} className="registration-form">
        {error && <div className="registration-error">{error}</div>}

        <div className="form-group">
          <label>Эл. почта</label>
          <input
            name="email"
            type="email"
            placeholder="user@email.com"
            value={form.email}
            onChange={handleChange}
            required
            className="registration-input"
          />
        </div>

        <div className="form-group">
          <label>Логин</label>
          <input
            name="username"
            type="text"
            placeholder="andre123"
            value={form.username}
            onChange={handleChange}
            required
            className="registration-input"
          />
        </div>

        <div className="form-group">
          <label>Пароль</label>
          <input
            name="password"
            type="password"
            placeholder="Придумайте пароль"
            value={form.password}
            onChange={handleChange}
            required
            className="registration-input"
          />
        </div>

        <button type="submit" disabled={loading} className="registration-btn">
          {loading ? "Регистрация..." : "Зарегистрироваться"}
        </button>

        <div className="login-link">
          <Link to="/login">Уже есть аккаунт? Войти</Link>
        </div>
      </form>
      <SocialLoginButtons />
    </section>
  );
};

export default Registration;
