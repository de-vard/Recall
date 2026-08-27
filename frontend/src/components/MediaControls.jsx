import imageAdd from "../assets/add-image.png";
import imageDelete from "../assets/delete.png";
import audioAdd from "../assets/add-sound.png";

const MediaControls = ({
  card,
  fileInputRef,
  audioInputRef,
  handleChange,
  handleImageClick,
  handleAudioClick,
  onRemove,
  cardId,
}) => (
  <div className="card-controls">
    {/* Кнопка изображения */}
    <button type="button" className="icon-btn" onClick={handleImageClick}>
      <img src={imageAdd} alt="Добавить изображение" width={20} height={20} />
    </button>
    <input
      ref={fileInputRef}
      name="image"
      type="file"
      accept="image/*"
      onChange={handleChange}
      hidden
    />

    {/* Превью изображения */}
    {card.image && (
      <div className="media-preview">
        <img
          src={
            card.image instanceof File
              ? URL.createObjectURL(card.image)
              : card.image
          }
          alt="Preview"
          onLoad={(e) => {
            if (card.image instanceof File) URL.revokeObjectURL(e.target.src);
          }}
        />
        <div className="media-info">
          <span className="file-name">
            {card.image instanceof File
              ? card.image.name
              : "Текущее изображение"}
          </span>
          <button
            type="button"
            className="delete-btn"
            onClick={() => {
              handleChange({ target: { name: "image", value: null } });
              if (fileInputRef.current) fileInputRef.current.value = null;
            }}
          >
            ✕
          </button>
        </div>
      </div>
    )}

    {/* Аудио */}
    <button type="button" className="icon-btn" onClick={handleAudioClick}>
      <img src={audioAdd} alt="Добавить аудио" width={20} height={20} />
    </button>
    <input
      ref={audioInputRef}
      name="sound"
      type="file"
      accept="audio/*"
      onChange={handleChange}
      hidden
    />

    {card.sound && (
      <div className="media-preview">
        <audio
          controls
          src={
            card.sound instanceof File
              ? URL.createObjectURL(card.sound)
              : card.sound
          }
          onLoad={(e) => {
            if (card.sound instanceof File) URL.revokeObjectURL(e.target.src);
          }}
        />
        <div className="media-info">
          <span className="file-name">
            {card.sound instanceof File ? card.sound.name : "Текущее аудио"}
          </span>
          <button
            type="button"
            className="delete-btn"
            onClick={() => {
              handleChange({ target: { name: "sound", value: null } });
              if (audioInputRef.current) audioInputRef.current.value = null;
            }}
          >
            ✕
          </button>
        </div>
      </div>
    )}

    {/* Удаление карточки */}
    <button
      type="button"
      className="remove-btn"
      onClick={() => onRemove(cardId)}
    >
      <img src={imageDelete} alt="Удалить" width={25} height={25} />
    </button>
  </div>
);

export default MediaControls;
