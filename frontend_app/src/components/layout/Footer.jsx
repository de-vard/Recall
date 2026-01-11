import "../../styles/Footer.css";
import { useNavigate } from "react-router-dom";

const Footer = () => {
  const navigate = useNavigate();

  return (
    <footer className="footer">
      <button className="footer-btn" onClick={() => navigate(`/coming-soon`)}>
        Конфиденциальность
      </button>

      <button className="footer-btn" onClick={() => navigate(`/coming-soon`)}>
        Условия
      </button>

      <button className="footer-btn" onClick={() => navigate(`/coming-soon`)}>
        Язык
      </button>
    </footer>
  );
};

export default Footer;
