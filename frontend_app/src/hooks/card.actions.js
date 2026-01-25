import axiosService from "../utils/axios.js";
import { useState, useEffect } from "react";
import { CARD_ENDPOINTS } from "../utils/api.js";

export function useCard(public_id) {
  const [card, setCard] = useState(null);
  const [loading, setLoading] = useState(true); // Состояние загрузки данных
  const [error, setError] = useState(null); // Состояние ошибки

  const loadCard = async () => {
    setLoading(true);
    try {
      const { data } = await axiosService.get(
        
        CARD_ENDPOINTS.RETRIEVE(public_id),
      );
      setCard(data);
      setError(null);
    } catch (e) {
      const errorMessage =
        e.response?.data?.detail || e.message || "Ошибка загрузки;";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const createCard = (data) => axiosService.post(CARD_ENDPOINTS.CREATE, data);

  const editCard = (public_id, data) =>
    axiosService.patch(CARD_ENDPOINTS.PATCH(public_id), data);

  const deleteCard = (public_id) =>
    axiosService.delete(CARD_ENDPOINTS.DELETE(public_id));

  useEffect(() => {
    if (!public_id) return;
    loadCard();
  }, [public_id]);
  return { card, loading, error, loadCard, createCard, editCard, deleteCard };
}
