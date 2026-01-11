import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useUserActions } from "../../hooks/user.actions";
import "../../styles/Login.css"; // Добавляем импорт стилей

const Login = () => {
    const [form, setForm] = useState({ email: "", password: "" });
    const [error, setError] = useState(null);
    const login = useUserActions().login;

    const handleSubmit = (e) => {
        e.preventDefault();
        const data = { email: form.email, password: form.password };
        login(data).catch((err) => {
            if (err?.request?.response) {
                setError(err.request.response);
            } else {
                setError("Ошибка входа");
            }
        });
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    return (
        <section className="login-section">
            <h1>Вход</h1>
            <form onSubmit={handleSubmit} className="login-form">
                {error && <div className="login-error">{error}</div>}
                
                <div className="form-group">
                    <label>Эл. почта</label>
                    <input 
                        name="email"
                        placeholder="Введите адрес эл. почты"
                        type="email"
                        value={form.email}
                        onChange={handleChange}
                        className="login-input"
                    />
                </div>
                
                <div className="form-group">
                    <label>Пароль</label>
                    <input 
                        name="password"
                        placeholder="Введите пароль"
                        type="password"
                        value={form.password}
                        onChange={handleChange}
                        className="login-input"
                    />
                </div>
                
                <button type="submit" className="login-btn">Войти</button>
                
                <div className="register-link">
                    <Link to="/register/">
                        Впервые на сайте? Создать учетную запись
                    </Link>
                </div>
            </form>
        </section>
    );
};

export default Login;