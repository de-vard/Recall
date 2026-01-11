import axiosService from "../utils/axios.js";
import { useState, useEffect } from "react";
import { MODULE_ENDPOINTS } from "../utils/api.js";

export function useModule(public_id) {
    const [module, setModule] = useState(null);
    const [loading, setLoading] = useState(true);// Состояние загрузки данных
    const [error, setError] = useState(null); // Состояние ошибки

    const loadModule = async () => {
        setLoading(true);
        try {
            const { data } = await axiosService.get(MODULE_ENDPOINTS.RETRIEVE(public_id));
            setModule(data);
            setError(null);
        } catch (e) {
            const errorMessage = e.response?.data?.detail || e.message || "Ошибка загрузки;";
            setError(errorMessage)
        } finally {
            setLoading(false);
        }
    };

    const createModule = async (data) => {
        if (!data.title) return; //название обязательно
        const res = await axiosService.post(MODULE_ENDPOINTS.CREATE, data);
        return res.data;
    };

    const deleteModule = async()=>{
        const res = await axiosService.delete(MODULE_ENDPOINTS.DELETE(public_id));
        return res.data;
    };
    const editModule = async(data)=> {
        const res = await axiosService.patch(
            MODULE_ENDPOINTS.PATCH(public_id),
            data
        );
        if (public_id) await loadModule(); // <--- обновляем состояние
        return res.data;
    };


    useEffect(() => {
        if (!public_id) return;
        loadModule();
    }, [public_id]);
    return { module, loading, error, loadModule, createModule, deleteModule, editModule }
}