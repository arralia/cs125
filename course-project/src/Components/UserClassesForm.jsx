
export default function UserClassesForm({
  register,
  completedClasses,
  completedClassesAppend,
  completedClassesRemove,
  classListResponse,
  specializationListResponse,
}) {
  return (
    <div className="flex flex-col gap-4">
      {/* this section was written by gemini ai for the class selection, lke the 
      cards and the add class button and layout. I modified it to fit my needs. */}

      <div
        id="specialization"
        className="flex flex-col sm:flex-row gap-6 justify-between bg-white p-6 rounded-2xl border border-slate-200 shadow-sm"
      >
        <div className="flex flex-col gap-2 flex-1">
          <h3 className="text-lg font-bold text-slate-800">Specialization</h3>
          <select
            {...register("specialization")}
            className="w-full max-w-xs px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
          >
            <option value="">Select a specialization...</option>
            {specializationListResponse &&
              specializationListResponse.data &&
              specializationListResponse.data.map((spec, idx) => (
                <option key={idx} value={spec.specialization_name}>
                  {spec.specialization_name}
                </option>
              ))}
          </select>
        </div>

        <div className="flex flex-col gap-2">
          <h3 className="text-lg font-bold text-slate-800">Quarters Left</h3>

          <input
            type="number"
            min="0"
            {...register("quartersLeft", { valueAsNumber: true })}
            placeholder="e.g. 4"
            className="w-32 px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
          />
        </div>
      </div>

      <div id="classes" className="flex justify-between items-center mt-4 mb-2">
        <h3 className="text-xl font-bold text-slate-800">Classes Taken</h3>
        <button
          type="button"
          onClick={() =>
            completedClassesAppend({
              className: "",
              grade: "",
              difficulty: 3,
            })
          }
          className="bg-indigo-50 text-indigo-600 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-100 transition-colors shadow-sm"
        >
          + Add Class
        </button>
      </div>

      {(completedClasses?.length || 0) === 0 && (
        <div className="py-12 text-center border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50 text-slate-400">
          No classes added yet. Click "+ Add Class" to begin.
        </div>
      )}

      <div className="flex flex-col gap-3 max-h-[360px] overflow-y-auto pr-2 scrollbar-custom">
        {completedClasses?.map((classItem, index) => (
          <div
            key={classItem.id}
            className="flex flex-col sm:flex-row gap-4 bg-white p-5 rounded-2xl shadow-sm border border-slate-200 items-end hover:shadow-md transition-all"
          >
            <div className="flex-1 w-full">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                Class Name
              </label>
              <select
                {...register(`completedClasses.${index}.className`)}
                className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
              >
                <option value="">Select a class...</option>
                {classListResponse &&
                  classListResponse.data && // Access the 'data' array inside the object
                  Array.isArray(classListResponse.data) &&
                  classListResponse.data.map((course) => (
                    <option key={course.id} value={course.id}>
                      {course.id}
                    </option>
                  ))}
              </select>
            </div>

            <div className="w-full sm:w-28">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                Grade
              </label>
              <input
                type="text"
                placeholder="e.g. A-"
                {...register(`completedClasses.${index}.grade`)}
                className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
              />
            </div>

            <div className="w-full sm:w-40">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 text-center">
                Difficulty
              </label>
              <div className="flex gap-2 items-center px-2 py-2.5">
                <span className="text-xs font-semibold text-slate-400">1</span>
                <input
                  type="range"
                  min="1"
                  max="5"
                  {...register(`completedClasses.${index}.difficulty`, {
                    valueAsNumber: true,
                  })}
                  className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
                />
                <span className="text-xs font-semibold text-slate-400">5</span>
              </div>
            </div>

            <button
              type="button"
              onClick={() => completedClassesRemove(index)}
              className="p-3 text-red-500 bg-red-50 hover:bg-red-100 rounded-xl transition-colors"
              title="Remove Class"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                className="w-5 h-5"
              >
                <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
              </svg>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
