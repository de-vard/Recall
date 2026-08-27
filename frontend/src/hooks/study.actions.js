import axiosService from "../utils/axios.js";
import { useState, useEffect } from "react";
import { STUDY_ENDPOINTS } from "../utils/api.js";

export function useStudy(public_id) {
  const [study_cards, setStudy] = useState(null);
  const [loading, setLoading] = useState(true); // Состояние загрузки данных
  const [error, setError] = useState(null); // Состояние ошибки

  const loadStudy = async () => {
    setLoading(true);
    try {
      const { data } = await axiosService.get(
        STUDY_ENDPOINTS.RETRIEVE(public_id),
      );
      setStudy(data);
      setError(null);
    } catch (e) {
      const errorMessage =
        e.response?.data?.detail || e.message || "Ошибка загрузки;";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const createStudy = ( data) => axiosService.post(STUDY_ENDPOINTS.POST(public_id), data);

  const deleteStudy = () => axiosService.delete(STUDY_ENDPOINTS.DELETE(public_id));

  useEffect(() => {
    if (!public_id) return;
    loadStudy();
  }, [public_id]);

  return { study_cards, loading, error, loadStudy, createStudy, deleteStudy};
}
