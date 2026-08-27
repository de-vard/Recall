import React from "react";
import { Link } from "react-router-dom";
import "../../styles/FolderActions.css";

import courseEdit from "../../assets/edit.png";
import courseAdd from "../../assets/add.png";
import courseDelete from "../../assets/delete.png";



const CourseActionButtons = (props) => {

  return (
    <div className="folder-actions">
      <Link to={`/course/edit/${props.public_id}`}>
        <img src={courseEdit} alt="редактировать" width={30} height={30} />
      </Link>
      <Link to={`/module/create/${props.public_id}`}>
        <img src={courseAdd} alt="Создать" width={30} height={30} />
      </Link>
      <Link to={`/course/delete/${props.public_id}`}>
        <img src={courseDelete} alt="Удалить" width={30} height={30} />
      </Link>
    </div>
  );
};

export default CourseActionButtons;
