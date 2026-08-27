import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosService from "../../utils/axios";
import "../../styles/EmailVerificationNotice.css";

const REDIRECT_SECONDS = 15;

const EmailVerificationNotice = ({ email }) => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [secondsLeft, setSecondsLeft] = useState(REDIRECT_SECONDS);

  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          navigate("/login");
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [navigate]);

  const resendEmail = async () => {
    setLoading(true);
    setError(null);
    setMessage(null);

    try {
      await axiosService.post("/api/v1/auth/resend-verification/", { email });
      setMessage("Письмо отправлено повторно. Проверьте почту 📩");
    } catch (e) {
      setError("Не удалось отправить письмо");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="em-ver-container">
      <div className="em-ver-card">
        <h1>Подтвердите email</h1>

        <p className="em-ver-main-text">
          Мы отправили письмо на <b>{email}</b>.<br />
          Перейдите по ссылке из письма, чтобы активировать аккаунт.
        </p>

        <p className="em-ver-warning-text">
          ⚠️ Наш почтовый сервер недавно развернут на домене, поэтому первые
          письма могут попадать в <b>Спам</b>.<br />
          Пожалуйста, проверьте папку «Спам» и при необходимости отметьте письмо
          как «Не спам».
        </p>

        <button className="em-ver-button" onClick={resendEmail} disabled={loading}>
          {loading ? "Отправка..." : "Отправить письмо ещё раз"}
        </button>

        {message && <p className="em-ver-success">{message}</p>}
        {error && <p className="em-ver-error">{error}</p>}

        <div className="em-ver-redirect-timer">
          <p>Переход на страницу входа через:</p>
          <div className="em-ver-vintage-clock">
            <div className="em-ver-clock-face">
              <div className="em-ver-roman-markers">
                <div className="em-ver-marker" style={{ "--rot": 0 }} data-number="XII"></div>
                <div className="em-ver-marker" style={{ "--rot": 30 }} data-number="I"></div>
                <div className="em-ver-marker" style={{ "--rot": 60 }} data-number="II"></div>
                <div className="em-ver-marker" style={{ "--rot": 90 }} data-number="III"></div>
                <div className="em-ver-marker" style={{ "--rot": 120 }} data-number="IV"></div>
                <div className="em-ver-marker" style={{ "--rot": 150 }} data-number="V"></div>
                <div className="em-ver-marker" style={{ "--rot": 180 }} data-number="VI"></div>
                <div className="em-ver-marker" style={{ "--rot": 210 }} data-number="VII"></div>
                <div className="em-ver-marker" style={{ "--rot": 240 }} data-number="VIII"></div>
                <div className="em-ver-marker" style={{ "--rot": 270 }} data-number="IX"></div>
                <div className="em-ver-marker" style={{ "--rot": 300 }} data-number="X"></div>
                <div className="em-ver-marker" style={{ "--rot": 330 }} data-number="XI"></div>
              </div>
              
              <div
                className="em-ver-hand em-ver-second-hand"
                style={{
                  transform: `rotate(${secondsLeft * 6}deg)`,
                  transition: "transform 0.9s cubic-bezier(0.4, 0, 0.2, 1)",
                }}
              />
              <div className="em-ver-hand em-ver-minute-hand" />
              <div className="em-ver-hand em-ver-hour-hand" />

              <div className="em-ver-center-dot" />
            </div>

            <div className="em-ver-seconds-text">{secondsLeft}</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default EmailVerificationNotice;