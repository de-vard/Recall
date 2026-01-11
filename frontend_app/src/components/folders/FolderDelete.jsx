import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useFolder } from "../../hooks/folder.actions";
import "../../styles/FolderDelete.css";

const FolderDelete = () => {
  const [error, setError] = useState(null);
  const { public_id } = useParams();
  const { folder, deleteFolder } = useFolder(public_id);
  const navigate = useNavigate();

  const handleDelete = async () => {
    try {
      await deleteFolder();
      navigate(`/folder/${folder.parent_folder || "/"}`);
    } catch (err) {
      const data = err.response?.data;
      const msg =
        typeof data === "string"
          ? data
          : data
            ? Object.values(data)
            : "Ошибка сервера";
      setError(msg);
    }
  };

  const handleCancel = () => navigate(-1);

  return (
    <div className="folder-delete-page">
      <div className="folder-delete-card">
        <h1>Вы действительно хотите удалить папку?</h1>
        {error && <p className="error">{error}</p>}

        <div className="folder-delete-buttons">
          <button className="delete" onClick={handleDelete}>
            Да
          </button>
          <button className="cancel" onClick={handleCancel}>
            Нет
          </button>
        </div>
      </div>
    </div>
  );
};

export default FolderDelete;
