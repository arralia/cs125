import { useState, useEffect, useCallback, useRef } from "react";
import useApiGet from "../hooks/useApiGet";
import ClassCardCollection from "../Components/ClassCardCollection";
import { ReadCookie } from "../Components/CookieUtils";
import { ListFilter } from "lucide-react";
import ClassFiltersForm from "../Components/ClassFiltersForm";

export default function RecommendedCoursesPage() {
  const [recommendedClasses, setRecommendedClasses] = useState([]);
  const [username, setUsername] = useState(() => ReadCookie("username") || "");
  const [showFilters, setShowFilters] = useState(false);
  const filterRef = useRef(null);

  const { execute } = useApiGet({
    api: "/api/recommendedClasses",
  });
  // TODO: better way to make sure recommended classes re-render than interval polling...
  const getRecommendedClasses = useCallback(
    (nextUsername) => {
      execute({ params: { username: nextUsername || "" } }).then((res) => {
        setRecommendedClasses(res.data);
      });
    },
    [execute],
  );

  useEffect(() => {
    const intervalId = setInterval(() => {
      const currentUsername = ReadCookie("username") || "";
      setUsername((prevUsername) =>
        prevUsername === currentUsername ? prevUsername : currentUsername,
      );
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {
    getRecommendedClasses(username);
  }, [getRecommendedClasses, username]);

  // Click outside handler written by gemini ai
  useEffect(() => {
    function handleClickOutside(event) {
      if (filterRef.current && !filterRef.current.contains(event.target)) {
        setShowFilters(false);
      }
    }

    if (showFilters) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showFilters]);

  return (
    <div className="flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 h-full">
      <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row justify-between items-start sm:items-center bg-slate-50/50 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800">
            Recommended for You
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Based on your interests and degree progress
          </p>
        </div>
        <div className="flex gap-2 items-center relative" ref={filterRef}>
          <button
            onClick={() => getRecommendedClasses(username)}
            className="text-sm font-semibold py-2 px-5 text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm shadow-indigo-200 rounded-xl transition-all hover:shadow-md cursor-pointer whitespace-nowrap"
          >
            Refresh Recommendations
          </button>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`text-sm font-semibold py-2 px-5 rounded-xl transition-all cursor-pointer whitespace-nowrap flex items-center justify-center ${
              showFilters
                ? "bg-slate-200 text-slate-700 shadow-inner"
                : "text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm shadow-indigo-200 hover:shadow-md"
            }`}
          >
            <ListFilter className="w-5 h-5" />
          </button>

          {showFilters && (
            <div className="absolute right-0 top-full mt-2 z-30 origin-top-right">
              <ClassFiltersForm
                recommendedClasses={recommendedClasses}
                setRecommendedClasses={setRecommendedClasses}
                setShowFilters={setShowFilters}
              />
            </div>
          )}
        </div>
      </div>
      <div className="p-6 flex-1 min-h-0 overflow-y-auto scrollbar-custom bg-slate-50/20">
        <ClassCardCollection
          data={recommendedClasses}
          className="grid-cols-1 sm:grid-cols-2"
        />
      </div>
    </div>
  );
}
