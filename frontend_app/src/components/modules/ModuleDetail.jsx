import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useModule } from "../../hooks/module.actions";
import ModuleActionButtons from "./ModuleActionButtons";
import "../../styles/ModuleDetail.css";

const ModuleDetail = () => {
  const { public_id } = useParams();
  const { module, loading, error } = useModule(public_id);
  const navigate = useNavigate();

  // Обрабатываем состояния загрузки и ошибки ПЕРВЫМИ
  if (loading) return <div className="loading">Загрузка...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;
  if (!module) return <div className="no-data">Нет данных о модуле</div>;
  const handleGoBack = () => {
    navigate(`/course/${module.course.public_id}`);
  };

  return (
    <div className="module-detail">
      <div className="back-button">
        <button onClick={handleGoBack}>← Назад</button>
      </div>

      <div className="module-header">
        <div className="module-info">
          <h2>Наименование модуля: {module.title}</h2>
          <strong>Принадлежит курсу: </strong>
          <a
            href={`/course/${module.course.public_id}`}
            className="course-link"
            onClick={(e) => {
              e.preventDefault();
              navigate(`/course/${module.course.public_id}`);
            }}
          >
            {module.course.title}
          </a>
        </div>
        <ModuleActionButtons public_id={public_id} />
      </div>

      <div className="action-buttons">
        <button className="primary" onClick={() => navigate(`/study/${public_id}`)}>
          Карточки
        </button>
        <button className="primary" onClick={() => navigate(`/coming-soon`)}>
          Заучивание
        </button>
        <button className="primary" onClick={() => navigate(`/coming-soon`)}>
          Тест
        </button>
        <button className="primary" onClick={() => navigate(`/history/${public_id}`)}>
          Прогресс
        </button>
      </div>

      <div className="module-cards-list">
        {module.cards.map((card, index) => (
          <div key={card.public_id} className="module-card-item">
            <span className="card-index-text">{index + 1}</span>

            <div className="module-card-content">
              {/* Левая колонка: термин и транскрипция */}
              <div className="module-card-left">
                <h3 className="module-card-term">{card.term}</h3>
                {card.transcription && (
                  <p className="module-card-transcription">
                    [{card.transcription}]
                  </p>
                )}
              </div>

              {/* Правая колонка: определение, картинка и звук */}
              <div className="module-card-right">
                <p className="module-card-definition">{card.definition}</p>

                <div className="module-card-media">
                  {card.image && (
                    <img
                      src={card.image}
                      alt={card.term}
                      className="module-card-image"
                    />
                  )}

                  {card.sound && (
                    <div className="module-card-audio">
                      <audio controls>
                        <source src={card.sound} />
                      </audio>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ModuleDetail;
