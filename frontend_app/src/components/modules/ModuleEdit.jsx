import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useModule } from "../../hooks/module.actions";
import { useCard } from "../../hooks/card.actions";
import { useMedia } from "../../hooks/media.actions";
import CardForm from "../CardForm";
import "../../styles/ModuleEdit.css";

const ModuleEdit = () => {
  const { public_id } = useParams();
  const navigate = useNavigate();

  const { module, editModule } = useModule(public_id);
  const [cards, setCards] = useState([]);
  const [title, setTitle] = useState("");
  const { deleteCard: deleteCardRequest, createCard } = useCard();
  const { uploadImage, uploadSound } = useMedia();
  const { editCard: editCardRequest } = useCard();
    
    
    
  // Функция для генерации уникального ID
  const generateUniqueId = () => {
    // Используем timestamp + случайное число
    return 'id-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
  };
  
  // Загружаем данные модуля в state
  useEffect(() => {
    if (!module) return;
    setTitle(module.title);
    setCards(
      module.cards.map((card) => ({
        ...card,
        id: card.public_id,
        image: card.image || null,
        sound: card.sound || null,
        isNew: false,
        isDeleted: false,
      })),
    );
  }, [module]);

  //Добавление новой карточки
  const addCard = () => {
    setCards((cards) => [
      ...cards,
      {
        id: generateUniqueId(),
        term: "",
        definition: "",
        transcription: "",
        image: null,
        sound: null,
        isNew: true,
      },
    ]);
  };

  const deleteCard = async (card) => {
    if (card.isNew) {
      setCards((prev) => prev.filter((c) => c !== card));
      return;
    }

    await deleteCardRequest(card.public_id);
    setCards((prev) => prev.filter((c) => c.public_id !== card.public_id));
  };

  const editCard = (cardId, field, value) => {
    setCards((prev) =>
      prev.map((card) =>
        card.id === cardId ? { ...card, [field]: value } : card,
      ),
    );
  };

  const handleCancel = () => {
    //При отмене удаления возвращаемся обратно
    navigate(-1); // возвращаемся назад
  };

  // Сохранение модуля и карточек
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // 1️⃣ (опционально) обновление модуля
      await editModule({ title });

      // 2️⃣ обработка карточек

      for (const card of cards) {
        // 🔹 загрузка изображения
        let image = undefined;
        
        if (card.image instanceof File) {
          const uploaded = await uploadImage(card.image);
          image = uploaded.public_id;
        } else if (card.image?.public_id) {
          image = card.image.public_id;
        }

        // 🔹 загрузка аудио
        let sound = undefined;
        if (card.sound instanceof File) {
          const uploaded = await uploadSound(card.sound);
          sound = uploaded.public_id;
        } else if (card.sound?.public_id) {
          sound = card.sound.public_id;
        }

        const payload = {
          term: card.term,
          definition: card.definition,
          transcription: card.transcription || null,
          image,
          sound,
        };

        // 🆕 новая карточка
        if (card.isNew) {
          await createCard({
            ...payload,
            flashcard: public_id,
          });
        }
        // ✏️ существующая карточка
        else {
          await editCardRequest(card.public_id, payload);
        }
      }

      // 3️⃣ переход обратно
      navigate(`/module/${public_id}`);
    } catch (err) {
      console.error("Ошибка сохранения модуля:", err);
      alert("Ошибка при сохранении. Попробуй ещё раз.", err);
    }
  };

  return (
 <div className="module-edit">
      <h1>Редактирование модуля</h1>
      
      <form onSubmit={handleSubmit} className="module-edit-form">
        <div className="module-title-group">
          <label>Название модуля</label>
          <input 
            value={title} 
            onChange={(e) => setTitle(e.target.value)}
            className="module-title-input"
            placeholder="Введите название модуля"
          />
        </div>

        {cards.map((card, index) => (
          <CardForm
            key={card.id}
            card={card}
            cardId={card.id}
            index={index}
            onChange={editCard}
            onRemove={() => deleteCard(card)}
          />
        ))}

        <div className="module-cards-actions">
          <button type="button" onClick={addCard} className="add-card-btn">
            ➕ Добавить слово
          </button>
        </div>

        <div className="module-form-actions">
          <button type="submit" className="save-btn">💾 Сохранить</button>
          <button type="button" onClick={handleCancel} className="cancel-btn">
            Назад
          </button>
        </div>
      </form>
    </div>
  );
};

export default ModuleEdit;