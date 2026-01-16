import axiosService from "../utils/axios";
import { useNavigate } from "react-router-dom";
import { USER_ENDPOINTS } from "../utils/api";

// Хук, который содержит функции для работы с пользователем:
// логин, регистрация, выход
function useUserActions() {
    const navigate = useNavigate(); // инструмент для перехода между страницами

    // Возвращаем функции, чтобы можно было использовать их в React-компонентах
    return {
        login,
        register,
        logout,
    };
    // ======= Вход пользователя =======
    function login(data) {
        // Отправляем POST-запрос на сервер с email + password
        return axiosService.post(USER_ENDPOINTS.LOGIN, data).then((res) => {
            // res.data содержит: access, refresh, user
            // Сохраняем эти данные в localStorage
            setUserData(res.data);

            // После успешного входа переходим на главную страницу
            navigate("/");
        });
    }

    // ======= Регистрация пользователя =======
    function register(data) {
        // Отправляем POST-запрос для регистрации
        return axiosService.post(USER_ENDPOINTS.REGISTER, data).then((res) => {
            // Сервер возвращает такие же данные: access, refresh, user
            setUserData(res.data);

            // Перенаправляем на главную после регистрации
            navigate("/");
        });
    }

    // ======= Выход пользователя =======
    function logout() {
        // Удаляем все данные пользователя и токены
        localStorage.removeItem("auth");

        // Переходим на страницу логина
        navigate("/login");
    }
}



// ======= Получить данные текущего пользователя =======
function getUser() {
    // Достаём объект auth из localStorage
    const auth = JSON.parse(localStorage.getItem("auth")) || {};
    // Возвращаем поле user или undefined
    return auth?.user;
}

// ======= Получить access token =======
function getAccessToken() {
    const auth = JSON.parse(localStorage.getItem("auth")) || {};
    return auth?.access;
}

// ======= Получить refresh token =======
function getRefreshToken() {
    const auth = JSON.parse(localStorage.getItem("auth")) || {};
    return auth?.refresh;
}

// ======= Сохранение данных пользователя и токенов =======
function setUserData(data) {
    // Сохраняем объект вида:
    // {
    //   access: "...",
    //   refresh: "...",
    //   user: {...}
    // }
    localStorage.setItem(
        "auth",
        JSON.stringify({
            access: data.access,
            refresh: data.refresh,
            user: data.user,
        })
    );
}

// Экспортируем функции для использования в приложении
export { useUserActions, getUser, getAccessToken, getRefreshToken };
