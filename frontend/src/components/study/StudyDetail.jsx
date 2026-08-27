import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useStudy } from "../../hooks/study.actions";
import "../../styles/StudyDetail.css";

const StudyDetail = () => {
  const { public_id } = useParams();
  const navigate = useNavigate();
  const { study_cards, loading, error, createStudy, deleteStudy, loadStudy } =
    useStudy(public_id);

  console.log("study_cards:", study_cards);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [isFlipped, setIsFlipped] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [autoPlaySound, setAutoPlaySound] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Один аудио-элемент на весь компонент
  const audioRef = useRef(null);
  // Текущий URL звука (меняется при смене карточки)
  const [currentSoundUrl, setCurrentSoundUrl] = useState(null);

  // Определяем текущую карточку
  const hasCards = study_cards && study_cards.length > 0;
  const currentCard = hasCards ? study_cards[currentIndex] : null;

  // Вычисляем, видна ли сейчас сторона с термином
  const isTermVisible = currentCard?.show_answer_first ? isFlipped : !isFlipped;

  // Обновляем src аудио при смене карточки
  useEffect(() => {
    if (currentCard?.sound) {
      setCurrentSoundUrl(currentCard.sound);
    } else {
      setCurrentSoundUrl(null);
    }
  }, [currentCard?.sound]);

  // Автопроигрывание: при смене звука или возврате на сторону с термином
  useEffect(() => {
    if (
      audioRef.current &&
      currentSoundUrl &&
      autoPlaySound &&
      isTermVisible &&
      hasCards
    ) {
      audioRef.current.currentTime = 0;
      audioRef.current.play().catch((err) => {
        console.log("Автопроигрывание заблокировано браузером:", err);
      });
    }
  }, [currentSoundUrl, isTermVisible, autoPlaySound, hasCards]);

  // Ранние возвраты (после всех хуков!)
  if (loading) return <div className="loading">Загрузка карточек...</div>;
  if (error) return <div className="error">Ошибка: {error}</div>;

  const handleAnswer = (isKnow) => {
    if (isSubmitting) return;

    const newAnswer = {
      card_id: currentCard.public_id,
      is_known: isKnow,
    };

    const newAnswers = [...answers, newAnswer];
    setAnswers(newAnswers);

    if (currentIndex < study_cards.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setIsFlipped(false);
    } else {
      const payload = { results: newAnswers };
      setIsSubmitting(true);
      createStudy(payload)
        .then(() => {
          alert("Сессия завершена! Прогресс сохранён.");
          navigate(`/module/${public_id}`);
        })
        .catch((err) => {
          console.error("Ошибка сохранения:", err.response?.data || err);
          alert("Не удалось сохранить прогресс.");
          setIsSubmitting(false);
        });
    }
  };

  const handleResetProgress = () => {
    if (
      !window.confirm(
        "Сбросить весь прогресс изучения этого набора? Вы снова увидите все карточки как новые.",
      )
    ) {
      return;
    }

    setIsDeleting(true);
    deleteStudy()
      .then(() => {
        alert("Прогресс успешно сброшен!");
        loadStudy();
        setCurrentIndex(0);
        setAnswers([]);
        setIsFlipped(false);
      })
      .catch((err) => {
        console.error("Ошибка сброса:", err);
        alert("Не удалось сбросить прогресс.");
      })
      .finally(() => {
        setIsDeleting(false);
      });
  };

  const handleFlip = () => {
    setIsFlipped(!isFlipped);
  };

  const toggleAutoPlay = (e) => {
    e.stopPropagation();
    setAutoPlaySound((prev) => !prev);
  };

  return (
    <div className="study-detail-container">
      {hasCards ? (
        <>
          <div
            className={`study-detail-flip-card ${isFlipped ? "study-detail-flipped" : ""}`}
            onClick={handleFlip}
          >
            <div className="study-detail-flip-card-inner">
              {/* ЛИЦЕВАЯ СТОРОНА */}
              <div className="study-detail-flip-card-front">
                {currentCard.show_answer_first ? (
                  // Показываем ответ (определение + картинка) первым
                  <>
                    {currentCard.image && (
                      <img src={currentCard.image} alt="Иллюстрация" />
                    )}
                    <p>{currentCard.definition}</p>
                  </>
                ) : (
                  // Показываем термин (слово + транскрипция + аудио) первым
                  <>
                    <h2>{currentCard.term}</h2>
                    {currentCard.transcription && (
                      <p>[{currentCard.transcription}]</p>
                    )}
                    <div className="study-detail-audio-container">
                      <audio
                        ref={audioRef}
                        controls
                        className="study-detail-card-audio"
                        src={currentSoundUrl || undefined}
                      >
                        Ваш браузер не поддерживает аудио.
                      </audio>
                      <button
                        className="study-detail-autoplay-toggle"
                        onClick={toggleAutoPlay}
                        onMouseDown={(e) => e.stopPropagation()}
                        title={
                          autoPlaySound
                            ? "Автопроигрывание включено"
                            : "Автопроигрывание выключено"
                        }
                      >
                        {autoPlaySound ? "🔊" : "🔇"}
                      </button>
                    </div>
                  </>
                )}
              </div>

              {/* ОБРАТНАЯ СТОРОНА */}
              <div className="study-detail-flip-card-back">
                {currentCard.show_answer_first ? (
                  // На обратной стороне показываем термин
                  <>
                    <h2>{currentCard.term}</h2>
                    {currentCard.transcription && (
                      <p>[{currentCard.transcription}]</p>
                    )}
                    <div className="study-detail-audio-container">
                      <audio
                        ref={audioRef}
                        controls
                        className="study-detail-card-audio"
                        src={currentSoundUrl || undefined}
                      >
                        Ваш браузер не поддерживает аудио.
                      </audio>
                      <button
                        className="study-detail-autoplay-toggle"
                        onClick={toggleAutoPlay}
                        onMouseDown={(e) => e.stopPropagation()}
                        title={
                          autoPlaySound
                            ? "Автопроигрывание включено"
                            : "Автопроигрывание выключено"
                        }
                      >
                        {autoPlaySound ? "🔊" : "🔇"}
                      </button>
                    </div>
                  </>
                ) : (
                  // На обратной стороне показываем ответ (определение + картинку)
                  <>
                    {currentCard.image && (
                      <img src={currentCard.image} alt="Иллюстрация" />
                    )}
                    <p>{currentCard.definition}</p>
                  </>
                )}
              </div>
            </div>
          </div>

          <div className="study-detail-progress-text">
            {currentIndex + 1} / {study_cards.length}
          </div>

          <div className="study-detail-answer-buttons">
            <button
              onClick={() => handleAnswer(true)}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Отправка..." : "Знаю"}
            </button>
            <button
              onClick={() => handleAnswer(false)}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Отправка..." : "Не знаю"}
            </button>
          </div>

          <button
            className="study-detail-reset-button"
            onClick={handleResetProgress}
            disabled={isDeleting}
          >
            {isDeleting
              ? "Сбрасываем прогресс..."
              : "Сбросить прогресс изучения"}
          </button>
        </>
      ) : (
        <div className="study-detail-congrats">
          <h2>🎉 Поздравляем!</h2>
          <p>Вы изучили все карточки в этом наборе.</p>
          <button
            className="study-detail-reset-button"
            onClick={handleResetProgress}
            disabled={isDeleting}
          >
            {isDeleting ? "Сбрасываем..." : "Сбросить прогресс изучения"}
          </button>
        </div>
      )}
    </div>
  );
};

export default StudyDetail;