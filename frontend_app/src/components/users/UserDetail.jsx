// src/components/users/UserDetail.jsx

import React from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getUser } from "../../hooks/user.actions";   // или user.secondActions — как у тебя
import { useUser } from "../../hooks/useUser";
import "../../styles/UserDetail.css";

const UserDetail = () => {
    const { public_id } = useParams();
    const navigate = useNavigate();

    const currentUser = getUser();
    const isOwnProfile = currentUser?.public_id === public_id;

    const { user, loading, error, toggleFollow } = useUser(public_id);

    if (loading) return <div className="loading-screen">Загрузка профиля...</div>;
    if (error) return <div className="error-screen">Ошибка: {error}</div>;
    if (!user) return <div className="not-found">Пользователь не найден</div>;

    // Нормализуем authored_courses — чтобы всегда был массив строк с названием
    const courseTitles = user.authored_courses?.map(course =>
        typeof course === 'string' ? course : course.title
    ) || [];
    console.log(user);
    return (
        <div className="user-profile-page">
            <button className="back-btn" onClick={() => navigate(-1)}>
                ← Назад
            </button>

            <div className="profile-card">
                <div className="avatar-wrapper">
                    {user.avatar ? (
                        <img src={user.avatar} alt={user.username} className="avatar" />
                    ) : (
                        <div className="avatar-placeholder">
                            {user.first_name?.[0] || '?'}{user.last_name?.[0] || '?'}
                        </div>
                    )}
                    {!isOwnProfile && user.is_online && <div className="online-indicator" />}
                </div>

                <div className="profile-main">
                    <h1 className="full-name">{user.first_name} {user.last_name}</h1>
                    <p className="username">@{user.username}</p>

                    {!isOwnProfile && (
                        <div className="status-row">
                            {user.is_online ? (
                                <span className="status online">● Сейчас онлайн</span>
                            ) : user.last_active ? (
                                <span className="status last-seen">
                                    Был(а) {new Date(user.last_active).toLocaleString('ru-RU')}
                                </span>
                            ) : null}
                        </div>
                    )}

                    {user.bio && <p className="bio">{user.bio}</p>}

                    <div className="stats">
                        <div className="stat">
                            <span className="stat-value">{courseTitles.length}</span>
                            <span className="stat-label">Курсов</span>
                        </div>
                        <div className="stat">
                            <span className="stat-value">{user.count_followers || 0}</span>
                            <span className="stat-label">Подписчики</span>
                        </div>
                        <div className="stat">
                            <span className="stat-value">{user.count_following || 0}</span>
                            <span className="stat-label">Подписки</span>
                        </div>
                    </div>

                    {!isOwnProfile && (
                        <button
                            className={`follow-btn ${user.is_following ? 'following' : ''}`}
                            onClick={() => toggleFollow(public_id)}
                        >
                            {user.is_following ? "✓ Вы подписаны" : "Подписаться"}
                        </button>
                    )}
                </div>
            </div>

            {/* Дополнительная информация только для своего профиля */}
            {isOwnProfile && (
                <div className="own-profile-info">
                    <h2>Моя информация</h2>
                    <p><strong>Email:</strong> {user.email}</p>

                    {user.studying_courses?.length > 0 && (
                        <div className="my-section">
                            <h3>Изучаю курсы ({user.studying_courses.length})</h3>
                            <ul>
                                {user.studying_courses.map((title, i) => (
                                    <li key={i}>{title}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {user.folders?.length > 0 && (
                        <div className="my-section">
                            <h3>Мои папки ({user.folders.length})</h3>
                            <ul>
                                {user.folders.map((folder, i) => (
                                    <li key={i}>{folder}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}

            {/* Секция курсов */}
            {courseTitles.length > 0 && (
                <div className="courses-section">
                    <h2 className="section-title">
                        {isOwnProfile ? "Мои курсы" : "Курсы автора"}
                        <span>({courseTitles.length})</span>
                    </h2>

                    <div className="courses-grid">
                        {user.authored_courses?.map((course) => {
                            // course может быть строкой или объектом
                            const title = typeof course === 'string' ? course : course.title;
                            const courseId = typeof course === 'string' ? null : course.public_id;

                            return (
                                <Link
                                    key={courseId || title}
                                    to={courseId ? `/course/${courseId}` : '#'}
                                    className="course-item"
                                >
                                    <div className="course-icon">📖</div>
                                    <div className="course-info">
                                        <h3>{title}</h3>
                                        {courseId && <p className="go-to">Перейти к курсу →</p>}
                                    </div>
                                </Link>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
};

export default UserDetail;