import { Link } from "react-router-dom";
import folderEdit from "../../assets/edit.png";
import folderAdd from "../../assets/add.png";
import folderAddFolder from "../../assets/add_.png";
import folderDelete from "../../assets/delete.png";
import "../../styles/FolderActions.css";

const FolderActionButtons = ({ public_id }) => {
  return (
    <div className="folder-actions">
      <Link to={`/folder/edit/${public_id}`} title="Редактировать">
        <img src={folderEdit} alt="Редактировать" />
      </Link>

      <Link to={`/folder/create/${public_id}`} title="Создать папку">
        <img src={folderAddFolder} alt="Создать папку" />
      </Link>

      <Link to={`/course/create/${public_id}`} title="Создать курс">
        <img src={folderAdd} alt="Создать курс" />
      </Link>

      <Link to={`/folder/delete/${public_id}`} title="Удалить папку">
        <img src={folderDelete} alt="Удалить" />
      </Link>
    </div>
  );
};

export default FolderActionButtons;
