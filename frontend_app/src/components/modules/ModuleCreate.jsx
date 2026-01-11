import React, { useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useModule } from "../../hooks/module.actions";
import { useCard } from "../../hooks/card.actions";
import { useMedia } from "../../hooks/media.actions";
import CardForm from "../CardForm";
import "../../styles/ModuleCreate.css";

const ModuleCreate = () => {
    const { public_id } = useParams();
    const navigate = useNavigate();
    const { createModule } = useModule();
    const { createCard } = useCard();
    const { uploadImage, uploadSound } = useMedia();

    const [error, setError] = useState(null);
    const [form, setForm] = useState({ title: "", course: public_id });

    // Используем useRef для генерации уникальных id
    const nextCardId = useRef(1);

    const [cards, setCards] = useState([
        {
            id: nextCardId.current++,
            term: "",
            definition: "",
            transcription: "",
            image: null,
            sound: null,
        },
    ]);

    // Ошибки теперь хранятся по card.id (не по индексу!)
    const [validationErrors, setValidationErrors] = useState({});
    const [showValidationErrors, setShowValidationErrors] = useState(false);

    const addCard = () => {
        setCards((prev) => [
            ...prev,
            {
                id: nextCardId.current++,
                term: "",
                definition: "",
                transcription: "",
                image: null,
                sound: null,
            },
        ]);
    };

    const removeCard = (cardId) => {
        setCards((prev) => prev.filter((card) => card.id !== cardId));

        // Удаляем ошибки для этой карточки
        setValidationErrors((prev) => {
            const newErrors = { ...prev };
            delete newErrors[cardId];
            return newErrors;
        });
    };

    const updateCard = (cardId, field, value) => {
        setCards((prev) =>
            prev.map((card) =>
                card.id === cardId ? { ...card, [field]: value } : card
            )
        );

        // Очищаем ошибку для этого поля
        setValidationErrors((prev) => {
            const newErrors = { ...prev };
            if (newErrors[cardId] && newErrors[cardId][field]) {
                delete newErrors[cardId][field];
                if (Object.keys(newErrors[cardId]).length === 0) {
                    delete newErrors[cardId];
                }
            }
            return newErrors;
        });
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });

        // Очищаем ошибку названия модуля
        if (e.target.name === "title" && validationErrors.title) {
            setValidationErrors((prev) => {
                const newErrors = { ...prev };
                delete newErrors.title;
                return newErrors;
            });
        }
    };

    const validateForm = () => {
        const errors = {};

        // Название модуля
        if (!form.title.trim()) {
            errors.title = "Название модуля обязательно";
        }

        // Карточки
        cards.forEach((card) => {
            const cardErrors = {};

            if (!card.term.trim()) {
                cardErrors.term = "Термин обязателен";
            }
            if (!card.definition.trim()) {
                cardErrors.definition = "Определение обязательно";
            }

            if (Object.keys(cardErrors).length > 0) {
                errors[card.id] = cardErrors;
            }
        });

        // Хотя бы одна карточка
        if (cards.length === 0) {
            errors.cards = "Добавьте хотя бы одну карточку";
        }

        setValidationErrors(errors);
        setShowValidationErrors(true);

        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!validateForm()) {
            setError("Исправьте ошибки в форме");
            return;
        }

        try {
            const module = await createModule(form);

            if (!module?.public_id) {
                throw new Error("Модуль не создан");
            }

            for (const card of cards) {
                let imageId = null;
                let soundId = null;

                if (card.image instanceof File) {
                    const image = await uploadImage(card.image);
                    imageId = image.public_id || image.id;
                }

                if (card.sound instanceof File) {
                    const sound = await uploadSound(card.sound);
                    soundId = sound.public_id || sound.id;
                }

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
                        <p className="module-error">
                            {validationErrors.title}
                        </p>
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
                    <button 
                        type="button" 
                        onClick={addCard} 
                        className="action-btn primary"
                    >
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