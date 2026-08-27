import { Link } from "react-router-dom";
import courseIcon from "../../assets/course.png";
import folderIcon from "../../assets/folder.png";
import FolderActionButtons from "./FolderActionButtons";
import "../../styles/FolderContents.css";

const FolderContents = ({ list = [], public_id }) => {
  return (
    <div className="folder-wrapper">
      <FolderActionButtons public_id={public_id} />

      {list.length === 0 ? (
        <p className="empty-folder">
          У вас нет данных в папке ... 😢
        </p>
      ) : (
        <div className="folder-grid">
          {list.map((item) => (
            <Link
              key={item.public_id}
              to={`/${item.type}/${item.public_id}`}
              className="folder-card"
            >
              <img
                src={item.type === "folder" ? folderIcon : courseIcon}
                alt={item.type === "folder" ? "Папка" : "Курс"}
              />
              <span>{item.title}</span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default FolderContents;
