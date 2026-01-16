import React, { useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import CardForm from "../CardForm";
import "../../styles/ModuleCreate.css";

// Хуки для API
import { useModule } from "../../hooks/module.actions";
import { useCard } from "../../hooks/card.actions";
import { useMedia } from "../../hooks/media.actions";

const ModuleCreate = () => {
  const { public_id } = useParams();
  const navigate = useNavigate();
  const { createModule } = useModule();
  const { createCard } = useCard();
  const { uploadImage, uploadSound } = useMedia();

  const [form, setForm] = useState({ title: "", course: public_id });
  const [cards, setCards] = useState([
    { id: 1, term: "", definition: "", transcription: "", image: null, sound: null },
  ]);
  const [nextCardId, setNextCardId] = useState(2);

  const [validationErrors, setValidationErrors] = useState({});
  const [showValidationErrors, setShowValidationErrors] = useState(false);
  const [error, setError] = useState(null);

  // --- Обновление формы ---
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });

    if (e.target.name === "title" && validationErrors.title) {
      setValidationErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors.title;
        return newErrors;
      });
    }
  };

  // --- Управление карточками ---
  const addCard = () => {
    setCards((prev) => [
      ...prev,
      { id: nextCardId, term: "", definition: "", transcription: "", image: null, sound: null },
    ]);
    setNextCardId((prev) => prev + 1);
  };

  const removeCard = (cardId) => {
    setCards((prev) => prev.filter((card) => card.id !== cardId));
    setValidationErrors((prev) => {
      const newErrors = { ...prev };
      delete newErrors[cardId];
      return newErrors;
    });
  };

  const updateCard = (cardId, field, value) => {
    setCards((prev) =>
      prev.map((card) => (card.id === cardId ? { ...card, [field]: value } : card))
    );

    setValidationErrors((prev) => {
      const newErrors = { ...prev };
      if (newErrors[cardId] && newErrors[cardId][field]) {
        delete newErrors[cardId][field];
        if (Object.keys(newErrors[cardId]).length === 0) delete newErrors[cardId];
      }
      return newErrors;
    });
  };

  // --- Валидация ---
  const validateForm = () => {
    const errors = {};

    if (!form.title.trim()) errors.title = "Название модуля обязательно";

    if (cards.length === 0) errors.cards = "Добавьте хотя бы одну карточку";

    cards.forEach((card) => {
      const cardErrors = {};
      if (!card.term.trim()) cardErrors.term = "Термин обязателен";
      if (!card.definition.trim()) cardErrors.definition = "Определение обязательно";
      if (Object.keys(cardErrors).length > 0) errors[card.id] = cardErrors;
    });

    setValidationErrors(errors);
    setShowValidationErrors(true);

    return Object.keys(errors).length === 0;
  };

  // --- Отправка формы ---
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!validateForm()) {
      setError("Исправьте ошибки в форме");
      return;
    }

    try {
      // 1️⃣ Создаём модуль
      const module = await createModule(form);
      if (!module?.public_id) throw new Error("Модуль не создан");

      // 2️⃣ Загружаем карточки
      for (const card of cards) {
        let imageId = null;
        let soundId = null;

        // Загрузка изображения
        if (card.image instanceof File) {
          const uploadedImage = await uploadImage(card.image);
          imageId = uploadedImage.public_id;
        }

        // Загрузка аудио
        if (card.sound instanceof File) {
          const uploadedSound = await uploadSound(card.sound);
          soundId = uploadedSound.public_id;
        }

        // Создание карточки
        const payload = {
          term: card.term.trim(),
          definition: card.definition.trim(),
          transcription: card.transcription?.trim() || null,
          flashcard: module.public_id,
          image: imageId,
          sound: soundId,
        };

        await createCard(payload);
      }

      navigate(`/course/${public_id}`);
    } catch (err) {
      console.error(err);
      setError("Ошибка при создании модуля");
    }
  };

  return (
    <div className="module-create">
      <h1>Создание модуля/набора</h1>

      <form onSubmit={handleSubmit} className="module-form">
        {error && <div className="global-error">{error}</div>}

        <div>
          <label>Наименование модуля/набора*</label>
          <input
            name="title"
            type="text"
            value={form.title}
            onChange={handleChange}
            className={`module-input ${showValidationErrors && validationErrors.title ? "error" : ""}`}
          />
          {showValidationErrors && validationErrors.title && (
            <p className="module-error">{validationErrors.title}</p>
          )}
        </div>

        {cards.map((card, index) => (
          <CardForm
            key={card.id}
            card={card}
            cardId={card.id}
            index={index}
            onChange={updateCard}
            onRemove={removeCard}
            errors={validationErrors[card.id] || {}}
            showErrors={showValidationErrors}
          />
        ))}

        <div className="cards-actions">
          <button type="button" onClick={addCard} className="action-btn primary">
            ➕ Добавить слово
          </button>
        </div>

        {showValidationErrors && validationErrors.cards && (
          <p className="module-error">{validationErrors.cards}</p>
        )}

        <button type="submit" className="submit-btn">Создать</button>
      </form>
    </div>
  );
};

export default ModuleCreate;
