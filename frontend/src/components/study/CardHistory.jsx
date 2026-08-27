import React, { useState } from "react";
import { useHistoryCard } from "../../hooks/history.actions";

const CardHistory = (props) => {
  const { history_card, loading, error } = useHistoryCard(props.public_id);
  const [expanded, setExpanded] = useState(false);
  
  if (loading) return (
    <div className="loading-small">
      <div className="spinner-small"></div>
      <span>Загрузка истории...</span>
    </div>
  );
  
  if (error) return (
    <div className="error-small">
      <span>Ошибка загрузки истории</span>
    </div>
  );
  
  if (!history_card || !Array.isArray(history_card) || history_card.length === 0) {
    return (
      <div className="no-history">
        <p>Нет истории для этой карточки</p>
      </div>
    );
  }

  // Расчет статистики карточки
  const totalAttempts = history_card.length;
  const knownAttempts = history_card.filter(item => item.is_known).length;
  const successRate = (knownAttempts / totalAttempts) * 100;
  const lastAttempt = history_card[0]; // Последний ответ
  
  return (
    <div className="card-history">
      <div className="history-summary" onClick={() => setExpanded(!expanded)}>
        <div className="summary-stats">
          <span className="stat-badge attempts">
            Попыток: <strong>{totalAttempts}</strong>
          </span>
          <span className="stat-badge known">
            Известно: <strong>{knownAttempts}</strong>
          </span>
          <span className={`stat-badge rate ${successRate > 70 ? 'good' : successRate > 40 ? 'medium' : 'poor'}`}>
            Успешность: <strong>{successRate.toFixed(1)}%</strong>
          </span>
        </div>
        <div className="expand-toggle">
          {expanded ? 'Скрыть детали' : 'Показать детали'}
        </div>
      </div>
      
      {expanded && (
        <div className="history-details">
          <h5>История ответов:</h5>
          <div className="history-list">
            {history_card.map((item, index) => (
              <div key={index} className={`history-item ${item.is_known ? 'known' : 'unknown'}`}>
                <div className="item-header">
                  <span className="attempt-number">Попытка #{totalAttempts - index}</span>
                  <span className="item-date">
                    {new Date(item.date_answer).toLocaleString()}
                  </span>
                </div>
                <div className="item-status">
                  Статус: <strong>{item.is_known ? '✅ Знаю' : '❌ Не знаю'}</strong>
                </div>
                <div className="item-session">
                  ID сессии: <code>{item.session_id}</code>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default CardHistory;