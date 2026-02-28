import useApiGet from "../hooks/useApiGet";
import { useEffect, useState, useRef, useCallback } from "react";
import ClassCardCollection from "../Components/ClassCardCollection";
import { ChevronDownIcon, ListFilter } from "lucide-react";
import ClassFiltersForm from "../Components/ClassFiltersForm";

export default function CoursesPage() {
  const [classes, setClasses] = useState([]);
  const [selectedQuarter, setSelectedQuarter] = useState("All Courses");
  const [showFilters, setShowFilters] = useState(false);
  const filterRef = useRef(null);

  // Destructure the values from your hook
  const { execute } = useApiGet({
    api: "/api/allClassesData",
  });

  const fetchClasses = useCallback(() => {
    execute().then((res) => {
      setClasses(res?.data);
    });
  }, [execute]);

  // Use useEffect to trigger the fetch once
  useEffect(() => {
    fetchClasses();
  }, [fetchClasses, selectedQuarter]);

  // Click outside handler
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
      <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex flex-row justify-between items-center gap-4">
        <div className="flex flex-col">
          <h2 className="text-xl font-bold text-slate-800">All CS Courses</h2>
          <p className="text-sm text-slate-500 mt-1">Explore the courses</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <select
              value={selectedQuarter}
              onChange={(e) => setSelectedQuarter(e.target.value)}
              className="appearance-none text-sm font-semibold py-2 pl-5 pr-10 text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm shadow-indigo-200 rounded-xl transition-all hover:shadow-md cursor-pointer outline-none"
            >
              <option value="All Courses" className="text-slate-900">
                All Courses
              </option>
              <option value="Spring 2026" className="text-slate-900">
                Spring 2026
              </option>
              <option value="Winter 2026" className="text-slate-900">
                Winter 2026
              </option>
              <option value="Fall 2025" className="text-slate-900">
                Fall 2025
              </option>
            </select>
            <div className="absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none text-white/80">
              <ChevronDownIcon className="w-4 h-4 stroke-[3]" />
            </div>
          </div>

          <div className="relative" ref={filterRef}>
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
                  courses={classes}
                  setCourses={setClasses}
                  setShowFilters={setShowFilters}
                  fetchClasses={fetchClasses}
                />
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="p-6 flex-1 min-h-0 overflow-y-auto scrollbar-custom ">
        <ClassCardCollection data={classes} className="grid-cols-1" />
      </div>
    </div>
  );
}
