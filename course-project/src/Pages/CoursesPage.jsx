import useApiGet from "../hooks/useApiGet";
import { useEffect, useState, useRef, useCallback } from "react";
import ClassCardCollection from "../Components/ClassCardCollection";
import { ChevronDownIcon, ListFilter } from "lucide-react";
import ClassFiltersForm from "../Components/ClassFiltersForm";

export default function CoursesPage() {
  const [allClasses, setAllClasses] = useState([]);
  const [classes, setClasses] = useState([]);
  const [selectedQuarter, setSelectedQuarter] = useState("All Courses");
  const [quarters, setQuarters] = useState([]);
  const [showFilters, setShowFilters] = useState(false);
  const filterRef = useRef(null);

  // Destructure the values from your hook
  const { execute } = useApiGet({
    api: "/api/allClassesData",
  });

  const { execute: fetchQuarters } = useApiGet({
    api: "/api/quarters",
  });

  const fetchClasses = useCallback(() => {
    const paramQuarter = selectedQuarter === "All Courses" ? "" : selectedQuarter;
    execute({
      params: { quarter: paramQuarter },
    }).then((res) => {
      setAllClasses(res?.data || []);
      setClasses(res?.data || []);
    });
  }, [execute, selectedQuarter]);

  // Fetch quarters once
  useEffect(() => {
    fetchQuarters().then((res) => {
      if (res?.data) {
        setQuarters(res.data);
      }
    });
  }, [fetchQuarters]);

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
              className="appearance-none h-[40px] text-sm font-semibold py-2 pl-5 pr-10 text-slate-700 bg-white border border-slate-200 hover:border-slate-300 shadow-sm rounded-xl transition-all cursor-pointer outline-none focus:ring-2 focus:ring-indigo-500/20"
            >
              <option value="All Courses" className="text-slate-900">
                All Courses
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
                  courses={allClasses}
                  setCourses={setClasses}
                  setShowFilters={setShowFilters}
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
