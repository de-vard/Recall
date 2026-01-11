import axiosService from "../utils/axios.js";
import { useState, useEffect } from "react";
import { COURSE_ENDPOINTS } from "../utils/api.js";

export function useCourse(public_id) {
  const [course, setCourse] = useState(null); // текущий курс
  const [myCourses, setMyCourses] = useState(null); // мои курсы
  const [loading, setLoading] = useState(true); // Состояние загрузки данных
  const [error, setError] = useState(null); // Состояние ошибки

  const loadCourse = async () => {
    setLoading(true);
    try {
      const url = public_id
        ? COURSE_ENDPOINTS.RETRIEVE(public_id)
        : COURSE_ENDPOINTS.LIST;
      const { data } = await axiosService.get(url);
      setCourse(data);

      // мои курсы
      const { data: myData } = await axiosService.get(COURSE_ENDPOINTS.MY);
      setMyCourses(myData);

      setError(null);
    } catch (e) {
      const errorMessage =
        e.response?.data?.detail || e.message || "Ошибка загрузки;";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const createCourse = async (data) => {
    if (!data.title) return; //название обязательно
    const res = await axiosService.post(COURSE_ENDPOINTS.CREATE, data);
    return res.data;
  };

  const editCourse = async (data) => {
    const res = await axiosService.patch(
      COURSE_ENDPOINTS.PATCH(public_id),
      data,
    );
    if (public_id) await loadCourse(); // <--- обновляем состояние
    return res.data;
  };

  const deleteCourse = async () => {
    const res = await axiosService.delete(COURSE_ENDPOINTS.DELETE(public_id));
    return res.data;
  };

  const toggleReaction = async () => {
    const res = await axiosService.post(
      COURSE_ENDPOINTS.TOGGLE_REACTION(public_id),
    );
    if (public_id) await loadCourse(); // <--- обновляем состояние
    return res.data;
  };

  const toggleSubscription = async () => {
    const res = await axiosService.post(
      COURSE_ENDPOINTS.TOGGLE_SUBSCRIPTION(public_id),
    );
    if (public_id) await loadCourse(); // <--- обновляем состояние
    return res.data;
  };

  useEffect(() => {
    loadCourse();
  }, [public_id]);

  return {
    course,
    loading,
    error,
myCourses,
    loadCourse,
    createCourse,
    editCourse,
    deleteCourse,
    toggleReaction,
    toggleSubscription,
  };
}
