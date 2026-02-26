import { useState, useEffect, useCallback } from "react";
import useApiGet from "../hooks/useApiGet";
import ClassCardCollection from "../Components/ClassCardCollection";
import { ReadCookie } from "../Components/CookieUtils";
import { ListFilter } from "lucide-react";

export default function RecommendedCoursesPage() {
  const [recommendedClasses, setRecommendedClasses] = useState([]);
  const [username, setUsername] = useState(() => ReadCookie("username") || "");

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

  return (
    <div className="flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-full">
      <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row justify-between items-start sm:items-center bg-slate-50/50 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800">
            Recommended for You
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Based on your interests and degree progress
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => getRecommendedClasses(username)}
            className="text-sm font-semibold py-2 px-5 text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm shadow-indigo-200 rounded-xl transition-all hover:shadow-md cursor-pointer whitespace-nowrap"
          >
            Refresh Recommendations
          </button>
          <button
            onClick={() => getRecommendedClasses(username)}
            className="text-sm font-semibold py-2 px-5 text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm shadow-indigo-200 rounded-xl transition-all hover:shadow-md cursor-pointer whitespace-nowrap"
          >
            <ListFilter />
          </button>
        </div>
      </div>
      <div className="p-6 max-h-[600px] overflow-y-auto scrollbar-custom bg-slate-50/20">
        <e data={recommendedClasses} className="grid-cols-1 sm:grid-cols-2" />
      </div>
    </div>
  );
}
