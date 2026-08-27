import React, { useState, useRef } from "react";
import "../styles/CardForm.css"; // Подключите CSS-файл
import CardFields from "./CardFields";
import MediaControls from "./MediaControls";

const CardForm = ({ card, cardId, index, onChange, onRemove, errors = {}, showErrors = false }) => {
  const fileInputRef = useRef(null);
  const audioInputRef = useRef(null);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    onChange(cardId, name, files ? files[0] : value);
  };

  const handleImageClick = () => fileInputRef.current?.click();
  const handleAudioClick = () => audioInputRef.current?.click();

  const getError = (field) => showErrors && errors[field];

  return (
    <div className={`card-container ${getError("term") || getError("definition") ? "card-error" : ""}`}>
       <span className="card-index-text">{index + 1}</span>
      <CardFields card={card} handleChange={handleChange} getError={getError} />
      <MediaControls
        card={card}
        fileInputRef={fileInputRef}
        audioInputRef={audioInputRef}
        handleChange={handleChange}
        handleImageClick={handleImageClick}
        handleAudioClick={handleAudioClick}
        onRemove={onRemove}
        cardId={cardId}
      />
    </div>
  );
};

export default CardForm;
