// src/hooks/useUser.js

import { useState, useEffect } from "react";
import axiosService from "../utils/axios";
import { USER_ENDPOINTS } from "../utils/api";

export function useUser(public_id = null) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const loadUser = async () => {
        if (!public_id) {
            setLoading(false);
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const { data } = await axiosService.get(USER_ENDPOINTS.RETRIEVE(public_id));
            setUser(data);
        } catch (err) {
            const errorMsg = err.response?.data?.detail || err.message || "Не удалось загрузить профиль";
            setError(errorMsg);
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const toggleFollow = async () => {
        if (!user) return;

        try {
            await axiosService.post(USER_ENDPOINTS.FOLLOW(public_id));
            
            // Самый надёжный способ — просто перезагрузить данные с сервера
            await loadUser();
        } catch (err) {
            console.error("Ошибка при изменении подписки:", err);
            alert("Не удалось выполнить действие. Попробуйте позже.");
        }
    };

    useEffect(() => {
        loadUser();
    }, [public_id]);

    return {
        user,
        loading,
        error,
        toggleFollow,
        refreshUser: loadUser,
    };
}