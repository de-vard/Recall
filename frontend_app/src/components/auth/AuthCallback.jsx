// src/pages/AuthCallback.jsx
import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useUserActions } from "../../hooks/user.actions";

function AuthCallback() {
  const called = useRef(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { socialLogin } = useUserActions();

  useEffect(() => {
    if (called.current) return;
    called.current = true;

    const params = new URLSearchParams(location.search);
    const code = params.get("code");
    const error = params.get("error");
    const provider = params.get("state");

    if (error || !code || !provider) {
      alert("Ошибка авторизации");
      navigate("/login");
      return;
    }

    socialLogin(provider, code).catch(() => {
      alert("Не удалось войти через соцсеть");
      navigate("/login");
    });
  }, [location, socialLogin, navigate]);

  return <h2 style={{ textAlign: "center" }}>Выполняется вход…</h2>;
}

export default AuthCallback;
