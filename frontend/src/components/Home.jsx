import React from "react";
import { useFolder } from "../hooks/folder.actions";
import FolderContents from "../components/folders/FolderContents";
import "../styles/Home.css";

const Home = () => {
  const { folder, loading, error } = useFolder();

  if (loading) return <div className="home-state">Загрузка…</div>;
  if (error) return <div className="home-state error">Ошибка: {error}</div>;
  if (!folder) return <div className="home-state">Нет данных</div>;

  const contents = [
    ...folder.children.map((f) => ({ ...f, type: "folder" })),
    ...folder.courses.map((c) => ({ ...c, type: "course" })),
  ];

  return (
    <div className="home">
      <h1 style={{ textAlign: 'center' }}>Упорство и настойчивость - отрицательные качества. Если человек дурак.</h1>
      <FolderContents list={contents} public_id={folder.public_id} />
    </div>
  );
};

export default Home;
