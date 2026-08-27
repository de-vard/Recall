import axiosService from "../utils/axios.js";
import { useState, useEffect } from "react";
import { COURSE_ENDPOINTS } from "../utils/api.js";

export function useCourse(public_id, filters = {}) {
  const [course, setCourse] = useState(null); // текущий курс
  const [myCourses, setMyCourses] = useState(null); // мои курсы
  const [loading, setLoading] = useState(true); // Состояние загрузки данных
  const [error, setError] = useState(null); // Состояние ошибки
  const [totalCount, setTotalCount] = useState(0);

const loadCourse = async (pageNum = 1) => {
    setLoading(true);
    try {
      let url;

      if (public_id) {
        url = COURSE_ENDPOINTS.RETRIEVE(public_id);
      } else {
        const cleanFilters = Object.fromEntries(
          Object.entries(filters).filter(([_, v]) => v !== "" && v !== undefined && v !== null)
        );

        const limit = 25;
        const offset = (pageNum - 1) * limit;

        const params = new URLSearchParams({
          ...cleanFilters,
          limit,
          offset,
        }).toString();

        url = `${COURSE_ENDPOINTS.LIST}?${params}`;
      }

      const { data } = await axiosService.get(url);
      
      if (public_id) {
        setCourse(data);
      } else {
        setCourse(data);                    // {count, results}
        setTotalCount(data.count || 0);
      }

      // Загружаем "мои курсы"
      const { data: myData } = await axiosService.get(COURSE_ENDPOINTS.MY);
      setMyCourses(myData);

      setError(null);
    } catch (e) {
      const errorMessage = e.response?.data?.detail || e.message || "Ошибка загрузки";
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




  // Загрузка курса при монтировании / смене public_id
useEffect(() => {
    loadCourse(1);
  }, [public_id, JSON.stringify(filters)]);

  return {
    course,
    loading,
    error,
    totalCount,
    myCourses,
    loadCourse,
    createCourse,
    editCourse,
    deleteCourse,
    toggleReaction,
    toggleSubscription,
  };
}
