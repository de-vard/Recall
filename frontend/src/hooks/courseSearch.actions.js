import { useState, useEffect } from "react";
import axiosService from "../utils/axios";
import { COURSE_ENDPOINTS } from "../utils/api";

export function useCourseSearch(query) {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!query || query.trim() === "") {
      setResults([]);
      return;
    }

    const fetchSearch = async () => {
      setLoading(true);
      try {
        const { data } = await axiosService.get(
          COURSE_ENDPOINTS.SEARCH(query)
        );

        const items = Array.isArray(data)
          ? data
          : data.results || data.data || [];

        setResults(items);
        setError(null);
      } catch (e) {
        setError(e.response?.data?.detail || "Ошибка поиска");
      } finally {
        setLoading(false);
      }
    };

    fetchSearch();
  }, [query]);

  return { results, loading, error };
}