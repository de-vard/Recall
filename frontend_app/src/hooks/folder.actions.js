import axiosService from "../utils/axios.js";
import { useState, useEffect } from "react";
import { FOLDER_ENDPOINTS } from "../utils/api.js";

export function useFolder(public_id) {

    const [folder, setFolder] = useState(null);// Состояние текущей папки (данные с сервера)
    const [loading, setLoading] = useState(true);// Состояние загрузки данных
    const [error, setError] = useState(null); // Состояние ошибки

    const loadFolder = async () => {
        setLoading(true);
        try {
            const url = public_id ? FOLDER_ENDPOINTS.RETRIEVE(public_id) : FOLDER_ENDPOINTS.LIST;
            const { data } = await axiosService.get(url);
            setFolder(data);
            setError(null);
        } catch (e) {
            const errorMessage = e.response?.data?.detail || e.message || "Ошибка загрузки;";
            setError(errorMessage)
        } finally {
            setLoading(false);
        }
    };

    const editFolder = async (data) => {  
        if (!data.title) return; //название обязательно
        const res = await axiosService.patch(FOLDER_ENDPOINTS.PATCH(public_id),data);
        await loadFolder();// <--- обновляем состояние
        return res.data;
    };

    const createFolder = async(data)=>{
        // Создание папки
        if (!data.title) return; //название обязательно

        const res = await axiosService.post(FOLDER_ENDPOINTS.CREATE, data);
        await loadFolder(); // <--- обновляем состояние
        return res.data;
    };
    
    const deleteFolder = async() => {
        const res = await axiosService.delete(FOLDER_ENDPOINTS.DELETE(public_id))
        return res.data;
    };

    useEffect(
        () => { loadFolder(); }, [public_id]
    );

    return { folder, loading, error, loadFolder, editFolder, createFolder, deleteFolder};
}