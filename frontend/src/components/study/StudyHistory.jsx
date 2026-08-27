import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useModule } from "../../hooks/module.actions";
import { useHistorySession } from "../../hooks/history.actions";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, 
  PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line,
  AreaChart, Area
} from 'recharts';
import '../../styles//StudyHistory.css';

const StudyHistory = () => {
  const { public_id } = useParams();
  const { module, loading, error } = useModule(public_id);
  const { history_session, loading_s, error_s } = useHistorySession(public_id);
  const [expandedCard, setExpandedCard] = useState(null);

  if (loading || loading_s) return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Загрузка аналитики...</p>
    </div>
  );
  
  if (error || error_s) return (
    <div className="error-container">
      <div className="error-icon">⚠️</div>
      <h3>Ошибка загрузки</h3>
      <p>{error || error_s}</p>
    </div>
  );
  
  if (!module || !history_session) return (
    <div className="no-data">
      <h3>Нет данных о модуле</h3>
    </div>
  );
  console.log(history_session);
  // Расчет статистики
  const calculateStats = () => {
    const totalCards = module.cards.length;
    const totalSessions = history_session.length;
    const totalStudyTime = history_session.reduce((sum, session) => {
      const start = new Date(session.start_time);
      const end = new Date(session.end_time);
      return sum + (end - start);
    }, 0);
    
    const avgSessionTime = totalStudyTime / totalSessions;
    const totalKnownCards = history_session.reduce((sum, session) => sum + session.cards_known, 0);
    const avgKnownPerSession = totalKnownCards / totalSessions;
    
    return {
      totalCards,
      totalSessions,
      totalStudyTime: totalStudyTime / 1000, // в секундах
      avgSessionTime: avgSessionTime / 1000,
      totalKnownCards,
      avgKnownPerSession,
      completionRate: (totalKnownCards / (totalCards * totalSessions)) * 100
    };
  };

  const stats = calculateStats();
  
  // Данные для графиков
  const sessionData = history_session.map((session, index) => ({
    name: `Сессия ${index + 1}`,
    изучено: session.cards_studied,
    известно: session.cards_known,
    время: (new Date(session.end_time) - new Date(session.start_time)) / 1000,
    дата: new Date(session.start_time).toLocaleDateString()
  }));

  const performanceData = [
    { name: 'Изучено карточек', value: stats.totalKnownCards },
    { name: 'Всего сессий', value: stats.totalSessions },
    { name: 'Общее время', value: Math.round(stats.totalStudyTime / 60) } // в минутах
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="analytics-container">
      {/* Заголовок */}
      <div className="analytics-header">
        <h1 className="title">{module.title}</h1>
        <p className="subtitle">Курс: {module.course.title}</p>
      </div>

      {/* Общая статистика */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>{stats.totalCards}</h3>
            <p>Всего карточек</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🕒</div>
          <div className="stat-content">
            <h3>{stats.totalSessions}</h3>
            <p>Сессий изучения</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⏱️</div>
          <div className="stat-content">
            <h3>{Math.round(stats.totalStudyTime / 60)} мин</h3>
            <p>Общее время</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>{Math.round(stats.completionRate)}%</h3>
            <p>Прогресс изучения</p>
          </div>
        </div>
      </div>

      {/* Графики */}
      <div className="charts-container">
        <div className="chart-card">
          <h3>Продуктивность по сессиям</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sessionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="изучено" fill="#8884d8" name="Карточек изучено" />
              <Bar dataKey="известно" fill="#82ca9d" name="Карточек известно" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div className="chart-card">
          <h3>Время сессий</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={sessionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis label={{ value: 'Секунды', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Area type="monotone" dataKey="время" stroke="#ff7300" fill="#ff7300" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Круговой график */}
      <div className="chart-card full-width">
        <h3>Общая статистика</h3>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={performanceData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
              >
                {performanceData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* История сессий */}
      <div className="sessions-container">
        <h2>История сессий</h2>
        {history_session.length === 0 ? (
          <div className="empty-state">
            <p>Нет данных о сессиях изучения</p>
          </div>
        ) : (
          <div className="sessions-list">
            {history_session.map((session, index) => {
              const sessionDuration = (new Date(session.end_time) - new Date(session.start_time)) / 1000;
              const efficiency = session.cards_known / session.cards_studied * 100;
              
              return (
                <div key={index} className="session-card">
                  <div className="session-header">
                    <div className="session-badge">Сессия #{index + 1}</div>
                    <div className="session-date">
                      {new Date(session.start_time).toLocaleString()}
                    </div>
                  </div>
                  
                  <div className="session-stats">
                    <div className="stat-item">
                      <span className="stat-label">Длительность:</span>
                      <span className="stat-value">{sessionDuration} сек</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Изучено:</span>
                      <span className="stat-value">{session.cards_studied} карточек</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Известно:</span>
                      <span className="stat-value highlight">{session.cards_known} карточек</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Эффективность:</span>
                      <span className={`stat-value ${efficiency > 70 ? 'good' : efficiency > 40 ? 'medium' : 'poor'}`}>
                        {efficiency.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Карточки модуля */}
      <div className="cards-container">
        <h2>Карточки модуля ({module.cards.length})</h2>
        <div className="cards-grid">
          {module.cards.map((card, index) => (
            <div key={card.public_id} className="card-item">
              <div className="card-header" onClick={() => setExpandedCard(expandedCard === index ? null : index)}>
                <div className="card-number">{index + 1}</div>
                <div className="card-content">
                  <h4>{card.term}</h4>
                  <p>{card.definition}</p>
                  <p className="transcription">{card.transcription}</p>
                </div>
                <div className="card-arrow">
                  {expandedCard === index ? '▲' : '▼'}
                </div>
              </div>
              
              {expandedCard === index && (
                <div className="card-details">
                  {card.image && (
                    <div className="card-image">
                      <img src={card.image} alt={card.term} />
                    </div>
                  )}
                  {card.sound && (
                    <audio controls className="card-audio">
                      <source src={card.sound} type="audio/mpeg" />
                    </audio>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StudyHistory;