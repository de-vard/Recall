import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/UnderConstructionSculptor.css";
import GifHamer from "../assets/wallace-and-gromit.gif";

const UnderConstructionSculptor = () => {
  const navigate = useNavigate();

  return (
    <div className="ucs-wrapper">
      <div className="ucs-card">
        <img
          src={GifHamer}
          alt="Идут работы"
          className="ucs-hammer-gif"
        />

        <h2>Эта страница ещё не создана</h2>
        <p>Над ней ведутся работы</p>

        <button
          className="ucs-back-button"
          onClick={() => navigate(-1)}
        >
          Назад
        </button>
      </div>
    </div>
  );
};

export default UnderConstructionSculptor;
