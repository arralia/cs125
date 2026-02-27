import { useForm } from "react-hook-form";
import { useEffect } from "react";
import useApiGet from "../hooks/useApiGet";

export default function ClassFiltersForm({
  courses,
  setCourses,
  setShowFilters,
}) {
  const { register, handleSubmit } = useForm({
    defaultValues: {
      difficulty: 3,
      interests: [],
    },
  });

  const { execute: getInterestsList, response: interestsListResponse } =
    useApiGet({
      api: "/api/interestsList",
    });

  useEffect(() => {
    getInterestsList();
  }, [getInterestsList]);

  const onSubmit = (data) => {
    console.log("Filter Data:", data);
    setShowFilters(false);
    const filteredClasses = [];
    if (!courses) return;
    for (const course of courses) {
      const hasMatchingInterest =
        data.interests.length === 0 ||
        (Array.isArray(course.keywords) &&
        //&& course.difficulty <= data.difficulty filter for difficulty doesnt work yet since class doesnt have that attribute
          course.keywords.some((keyword) => data.interests.includes(keyword)));

      if (hasMatchingInterest) {
        filteredClasses.push(course);
      }
    }
    setCourses(filteredClasses);
  };
  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xl w-80 sm:w-96">
      <h2 className="text-2xl font-bold text-slate-800 mb-6">Class Filters</h2>

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-8">
        {/* Difficulty Slider */}
        <div className="flex flex-col gap-2">
          <div className="flex flex-row items-center justify-between gap-4">
            <label className="text-sm font-bold text-slate-500 uppercase tracking-wider whitespace-nowrap">
              Max Difficulty
            </label>
            <div className="flex gap-3 items-center flex-1 max-w-[200px]">
              <span className="text-xs font-semibold text-slate-400">1</span>
              <input
                type="range"
                min="1"
                max="5"
                step="1"
                {...register("difficulty", { valueAsNumber: true })}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
              />
              <span className="text-xs font-semibold text-slate-400">5</span>
            </div>
          </div>
        </div>

        {/* Interests Checkboxes */}
        <div className="flex flex-col gap-4">
          <label className="text-sm font-bold text-slate-500 uppercase tracking-wider">
            Interest Areas
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-[300px] overflow-y-auto pr-2 scrollbar-custom">
            {interestsListResponse &&
              interestsListResponse.data &&
              interestsListResponse.data.map((interest, idx) => (
                <label
                  key={idx}
                  className="flex items-center gap-3 p-3 rounded-xl border border-slate-100 hover:border-indigo-200 hover:bg-indigo-50/50 transition-all cursor-pointer group"
                >
                  <input
                    type="checkbox"
                    value={interest.keyword}
                    {...register("interests")}
                    className="w-5 h-5 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
                  />
                  <span className="text-slate-700 font-medium group-hover:text-indigo-700 transition-colors">
                    {interest.keyword}
                  </span>
                </label>
              ))}
            {/*this part is a place holder for loading, written by ai*/}
            {(!interestsListResponse || !interestsListResponse.data) && (
              <div className="animate-pulse flex flex-col gap-2">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="h-10 bg-slate-100 rounded-xl w-full"
                  />
                ))}
              </div>
            )}
          </div>
        </div>

        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-3 px-6 rounded-xl font-bold hover:bg-indigo-700 shadow-sm hover:shadow-md transition-all"
        >
          Apply Filters
        </button>
      </form>
    </div>
  );
}
