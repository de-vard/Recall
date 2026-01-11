import React from "react";
import { Link } from "react-router-dom";

import moduleEdit from "../../assets/edit.png";
import moduleDelete from "../../assets/delete.png";
import "../../styles/FolderActions.css";


const ModuleActionButtons = (props) => {

  return (
     <div className="folder-actions">
      <Link to={`/module/edit/${props.public_id}`}>
        <img src={moduleEdit} alt="редактировать" width={30} height={30} />
      </Link>
      <Link to={`/module/delete/${props.public_id}`}>
        <img src={moduleDelete} alt="Удалить" width={30} height={30} />
      </Link>
    </div>
  );
};

export default ModuleActionButtons;
