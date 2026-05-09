// src/hooks/useUser.js
import { useState, useEffect } from "react";
import axiosService from "../utils/axios";
import { USER_ENDPOINTS } from "../utils/api";

export function useUser(public_id = null, filters = {}) {
    const [user, setUser] = useState(null);
    const [users, setUsers] = useState([]);           
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [totalCount, setTotalCount] = useState(0);   // Добавлено для пагинации

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

    const loadUsers = async (pageNum = 1) => {          // Добавили параметр pageNum
        setLoading(true);
        setError(null);

        try {
            const cleanFilters = Object.fromEntries(
                Object.entries(filters).filter(([_, v]) => v !== "" && v !== undefined && v !== null)
            );

            const limit = 25;  // соответствует бэкенду
            const offset = (pageNum - 1) * limit;

            const params = new URLSearchParams({
                ...cleanFilters,
                limit,
                offset,
            }).toString();

            const url = `${USER_ENDPOINTS.LIST}${params ? `?${params}` : ''}`;

            const { data } = await axiosService.get(url);
            
            setUsers(data.results || data);           // LimitOffsetPagination возвращает {count, results}
            setTotalCount(data.count || 0);
        } catch (err) {
            const errorMsg = err.response?.data?.detail || err.message || "Не удалось загрузить пользователей";
            setError(errorMsg);
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const toggleFollow = async (targetPublicId = public_id) => {
        const idToUse = targetPublicId || public_id;
        
        if (!idToUse) {
            console.error("public_id отсутствует");
            return;
        }

        try {
            await axiosService.post(USER_ENDPOINTS.FOLLOW(idToUse));
            
            if (public_id) {
                await loadUser();
            } else {
                await loadUsers();          // обновляем текущую страницу списка
            }
        } catch (err) {
            console.error("Ошибка при изменении подписки:", err);
            if (public_id) await loadUser();
            else await loadUsers();
        }
    };

    useEffect(() => {
        if (public_id) {
            loadUser();
        } else {
            loadUsers(1);                   // Загружаем 1 страницу при старте
        }
    }, [public_id, JSON.stringify(filters)]);

    return {
        user,
        users,
        loading,
        error,
        totalCount,          // ← добавлено
        loadUsers,           // теперь принимает номер страницы
        toggleFollow,
        refreshUser: loadUser,
    };
}