const CardFields = ({ card, handleChange, getError }) => (
  <div className="card-content">
    <div className="card-fields">
      <div className="term-section">
        <div className={`input-wrapper ${getError("term") ? "input-error" : ""}`}>
          <textarea
            name="term"
            placeholder="Введите термин..."
            value={card.term || ""}
            onChange={handleChange}
          />
        </div>
        {getError("term") && <div className="error-text">{getError("term")}</div>}

        <input
          name="transcription"
          placeholder="Транскрипция (необязательно)"
          value={card.transcription || ""}
          onChange={handleChange}
          className="transcription-input"
        />
      </div>

      <div className="definition-section">
        <div className={`input-wrapper ${getError("definition") ? "input-error" : ""}`}>
          <textarea
            name="definition"
            placeholder="Введите определение..."
            value={card.definition || ""}
            onChange={handleChange}
          />
        </div>
        {getError("definition") && <div className="error-text">{getError("definition")}</div>}
      </div>
    </div>
  </div>
);

export default CardFields;
