import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useFolder } from "../../hooks/folder.actions";
import FolderContents from "./FolderContents";
import "../../styles/FolderDetail.css";

const FolderDetail = () => {
  const { public_id } = useParams();
  const navigate = useNavigate();
  const { folder, loading, error } = useFolder(public_id);

  if (loading) return <div className="folder-state">Загрузка...</div>;
  if (error) return <div className="folder-state error">Ошибка: {error}</div>;
  if (!folder) return <div className="folder-state">Нет данных</div>;

  const folders = folder.children.map((f) => ({ ...f, type: "folder" }));
  const courses = folder.courses.map((c) => ({ ...c, type: "course" }));
  const allContents = [...folders, ...courses];

  const handleGoBack = () => {
    if (folder.parent_title === "home" || !folder.parent_folder) {
      navigate("/");
    } else {
      navigate(`/folder/${folder.parent_folder}`);
    }
  };

  return (
    <div className="folder-detail-page">
      <h2 className="folder-title">Наименование папки: {folder.title}</h2>
      <FolderContents list={allContents} public_id={folder.public_id} />
      <button className="back-button" onClick={handleGoBack}>
        Назад
      </button>
    </div>
  );
};

export default FolderDetail;
