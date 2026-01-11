import axiosService from "../utils/axios.js";
import { useState, useEffect } from "react";
import { HISTORY_ENDPOINTS } from "../utils/api.js";

export function useHistoryCard(public_id) {
  const [history_card, setHistory] = useState(null);
  const [loading_c, setLoading] = useState(true); // Состояние загрузки данных
  const [error_c, setError] = useState(null); // Состояние ошибки

  const loadHistoryCard = async () => {
    setLoading(true);
    try {
      const { data } = await axiosService.get(
        HISTORY_ENDPOINTS.RETRIEVE_CARD(public_id),
      );
      setHistory(data);
      setError(null);
    } catch (e) {
      const errorMessage =
        e.response?.data?.detail || e.message || "Ошибка загрузки;";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!public_id) return;
    loadHistoryCard();
  }, [public_id]);

  return { history_card, loading_c, error_c, loadHistoryCard };
}

export function useHistorySession(public_id) {
  const [history_session, setHistory] = useState(null);
  const [loading_s, setLoading] = useState(true); // Состояние загрузки данных
  const [error_s, setError] = useState(null); // Состояние ошибки

  const loadHistorySession = async () => {
    setLoading(true);
    try {
      const { data } = await axiosService.get(
        HISTORY_ENDPOINTS.RETRIEVE_SESSIONS(public_id),
      );
      setHistory(data);
      setError(null);
    } catch (e) {
      const errorMessage =
        e.response?.data?.detail || e.message || "Ошибка загрузки;";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!public_id) return;
    loadHistorySession();
  }, [public_id]);

  return { history_session, loading_s, error_s, loadHistorySession };
}
