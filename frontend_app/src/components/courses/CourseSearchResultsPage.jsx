import { useSearchParams } from "react-router-dom";
import CourseSearchResults from "./CourseSearchResults";
import { useCourseSearch } from "../../hooks/courseSearch.actions";

const CourseSearchResultsPage = () => {
  const [params] = useSearchParams();
  const query = params.get("q") || "";

  const { results, loading } = useCourseSearch(query);

  return (
    <div className="courses-container">
      <h2 className="courses-title">
        Результаты поиска{query && `: «${query}»`}
      </h2>

      <CourseSearchResults results={results} loading={loading} />
    </div>
  );
};

export default CourseSearchResultsPage;