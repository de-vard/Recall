import github from "../../assets/github.png";
import google from "../../assets/google.png";
import "../../styles/SocialLoginButtons.css"; // отдельный файл стилей

function SocialLogin() {
  const GITHUB_CLIENT_ID = process.env.REACT_APP_GITHUB_CLIENT_ID;
  const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID;
  const REDIRECT_URI = process.env.REACT_APP_REDIRECT_URI;

  const handleGithubLogin = () => {
    const redirectUri = encodeURIComponent(REDIRECT_URI);
    const scope = encodeURIComponent("read:user user:email");

    window.location.href =
      `https://github.com/login/oauth/authorize` +
      `?client_id=${GITHUB_CLIENT_ID}` +
      `&redirect_uri=${redirectUri}` +
      `&scope=${scope}` +
      `&state=github`;
  };

  const handleGoogleLogin = () => {
    const redirectUri = encodeURIComponent(REDIRECT_URI);
    const scope = encodeURIComponent("openid email profile");

    window.location.href =
      `https://accounts.google.com/o/oauth2/v2/auth` +
      `?client_id=${GOOGLE_CLIENT_ID}` +
      `&redirect_uri=${redirectUri}` +
      `&response_type=code` +
      `&scope=${scope}` +
      `&state=google`;
  };

  return (
<div className="social-login-container">
      <p className="social-login-text">Или войдите через соцсети</p>
      <div className="social-buttons">
        <button className="social-btn github" onClick={handleGithubLogin}>
          <img src={github} alt="GitHub" className="social-icon" />
          Войти через GitHub
        </button>
        <button className="social-btn google" onClick={handleGoogleLogin}>
          <img src={google} alt="Google" className="social-icon" />
          Войти через Google
        </button>
      </div>
    </div>
  );
}

export default SocialLogin;
