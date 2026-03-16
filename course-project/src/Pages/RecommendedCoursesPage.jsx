import { useState, useEffect, useCallback } from "react";
import useApiGet from "../hooks/useApiGet";
import ClassCardCollection from "../Components/ClassCardCollection";
import { ReadCookie } from "../Components/CookieUtils";
import { ChevronDownIcon } from "lucide-react";

export default function RecommendedCoursesPage() {
  const [recommendedClasses, setRecommendedClasses] = useState([]);
  const [username, setUsername] = useState(() => ReadCookie("username") || "");
  const [selectedQuarter, setSelectedQuarter] = useState("All Quarters");
  const [quarters, setQuarters] = useState([]);

  const { execute } = useApiGet({
    api: "/api/recommendedClasses",
  });

  const { execute: fetchQuarters } = useApiGet({
    api: "/api/quarters",
  });

  // TODO: better way to make sure recommended classes re-render than interval polling...
  const getRecommendedClasses = useCallback(
    (nextUsername, quarterStr) => {
      const paramQuarter = quarterStr === "All Quarters" ? "" : quarterStr;
      execute({
        params: {
          username: nextUsername || "",
          quarter: paramQuarter,
        },
      }).then((res) => {
        setRecommendedClasses(res?.data || []);
        console.log("recommended classes: ", res?.data);
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
    fetchQuarters().then((res) => {
      if (res?.data) {
        setQuarters(res.data);
      }
    });
  }, [fetchQuarters]);

  useEffect(() => {
    getRecommendedClasses(username, selectedQuarter);
  }, [getRecommendedClasses, username, selectedQuarter]);

  return (
    <div className="flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 h-full">
      <div className="p-6 border-b border-slate-100 flex flex-col sm:flex-row justify-between items-start sm:items-center bg-slate-50/50 gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800">
            Classes Recommended for You
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Based on your interests and degree progress
          </p>
        </div>
        <div className="flex gap-4 items-center shrink-0">
          <div className="relative">
            <select
              value={selectedQuarter}
              onChange={(e) => setSelectedQuarter(e.target.value)}
              className="appearance-none h-[40px] text-sm font-semibold py-2 pl-5 pr-10 text-slate-700 bg-white border border-slate-200 hover:border-slate-300 shadow-sm rounded-xl transition-all cursor-pointer outline-none focus:ring-2 focus:ring-indigo-500/20"
            >
              <option value="All Quarters" className="text-slate-900">
                All Quarters
              </option>
              {quarters.map((q, idx) => (
                <option key={idx} value={`${q[1]} ${q[0]}`} className="text-slate-900">
                  {q[1]} {q[0]}
                </option>
              ))}
            </select>
            <div className="absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400">
              <ChevronDownIcon className="w-4 h-4 stroke-3" />
            </div>
          </div>
          <button
            onClick={() => getRecommendedClasses(username, selectedQuarter)}
            className="text-sm font-semibold h-[40px] px-5 text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm shadow-indigo-200 rounded-xl transition-all hover:shadow-md cursor-pointer whitespace-nowrap"
          >
            Load Recommendations
          </button>
        </div>
      </div>
      <div className="p-6 flex-1 overflow-y-auto scrollbar-custom bg-slate-50/20">
        <ClassCardCollection
          data={recommendedClasses}
          className="grid-cols-1 sm:grid-cols-2"
          showIndex={true}
        />
      </div>
    </div>
  );
}