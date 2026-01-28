import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useUserActions } from "../../hooks/user.actions";
import SocialLoginButtons from "./SocialLoginButtons";
import "../../styles/Registration.css"; // Добавляем импорт стилей

const Registration = () => {
    const navigate = useNavigate();
    const register = useUserActions().register;
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const [form, setForm] = useState({
        username: "",
        email: "",
        password: ""
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

            await register(formData);
          
        } catch (err) {
            if (err?.request?.response) {
                setError(err.request.response);
            } else {
                setError("Ошибка регистрации");
            }
        } finally {
            setLoading(false);
        }
    };

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

                <button 
                    type="submit" 
                    disabled={loading}
                    className="registration-btn"
                >
                    {loading ? "Регистрация..." : "Зарегистрироваться"}
                </button>

                <div className="login-link">
                    <Link to="/login">
                        Уже есть аккаунт? Войти
                    </Link>
                </div>
            </form>
            <SocialLoginButtons/>
        </section>
    );
};

export default Registration;