import { useState, useEffect, useCallback } from "react";
import useApiGet from "../hooks/useApiGet";
import ClassCardCollection from "../Components/ClassCardCollection";
import { ReadCookie } from "../Components/CookieUtils";

export default function RecommendedCoursesPage() {
  const [recommendedClasses, setRecommendedClasses] = useState([]);
  const [username, setUsername] = useState(() => ReadCookie("username") || "");
  const [isNextQuarterOnly, setIsNextQuarterOnly] = useState(true);

  const { execute } = useApiGet({
    api: "/api/recommendedClasses",
  });
  // TODO: better way to make sure recommended classes re-render than interval polling...
  const getRecommendedClasses = useCallback(
    (nextUsername, nextQuarterOnlyStr) => {
      execute({
        params: {
          username: nextUsername || "",
          next_quarter_only: nextQuarterOnlyStr,
        },
      }).then((res) => {
        setRecommendedClasses(res.data);
        console.log("recommended classes: ", res.data);
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
    getRecommendedClasses(username, isNextQuarterOnly);
  }, [getRecommendedClasses, username, isNextQuarterOnly]);

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
        <div className="flex gap-4 items-center shrink-0">
          <label className="flex items-center gap-3 cursor-pointer h-[40px] px-5 shadow-sm shadow-indigo-200 rounded-xl transition-all hover:shadow-md bg-indigo-600 hover:bg-indigo-700">
            <span className="text-sm font-semibold text-white select-none whitespace-nowrap">
              Next Quarter Only
            </span>
            <div className="relative flex items-center">
              <input
                type="checkbox"
                checked={isNextQuarterOnly}
                onChange={(e) => setIsNextQuarterOnly(e.target.checked)}
                className="peer sr-only"
              />
              <div className="h-5 w-10 rounded-full bg-white/20 transition-colors peer-checked:bg-emerald-600"></div>
              <div className="absolute left-0.5 top-0.5 h-4 w-4 rounded-full bg-white transition-transform peer-checked:translate-x-5 shadow-sm"></div>
            </div>
          </label>
          <button
            onClick={() => getRecommendedClasses(username, isNextQuarterOnly)}
            className="text-sm font-semibold h-[40px] px-5 text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm shadow-indigo-200 rounded-xl transition-all hover:shadow-md cursor-pointer whitespace-nowrap"
          >
            Load Recommendations
          </button>
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
