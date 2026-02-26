export default function UserInterestsForm({
  register,
  interests,
  interestsAppend,
  interestsRemove,
  interestsListResponse,
}) {
  return (
    <div className="flex flex-col gap-4">
      {/* this section was written orginally by gemini ai for the class selection, but i alterned it 
      to work with the interests section*/}

      <div className="flex justify-between items-center mb-2">
        <h3 className="text-xl font-bold text-slate-800">Your Interests</h3>
        <button
          type="button"
          onClick={() => interestsAppend({ interests: "" })}
          className="bg-indigo-50 text-indigo-600 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-100 transition-colors shadow-sm"
        >
          + Add Interest
        </button>
      </div>

      {interests?.length === 0 && (
        <div className="py-12 text-center border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50 text-slate-400">
          No interests added yet. Click "+ Add Interest" to begin.
        </div>
      )}

      <div className="flex flex-col gap-3 max-h-[400px] overflow-y-auto pr-2 scrollbar-custom">
        {interests?.map((interestsItem, index) => (
          <div
            key={interestsItem.id}
            className="flex flex-col sm:flex-row gap-4 bg-white p-5 rounded-2xl shadow-sm border border-slate-200 items-end hover:shadow-md transition-all"
          >
            <div className="flex-1 w-full">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                Interest Area
              </label>
              <select
                {...register(`interests.${index}.interests`)}
                className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all"
              >
                <option value="">Select an interest...</option>
                {interestsListResponse &&
                  interestsListResponse.data && // Access the 'data' array inside the object
                  Array.isArray(interestsListResponse.data) &&
                  interestsListResponse.data.map((interest, idx) => (
                    <option key={idx} value={interest.keyword}>
                      {interest.keyword}
                    </option>
                  ))}
              </select>
            </div>

            <button
              type="button"
              onClick={() => interestsRemove(index)}
              className="p-3 text-red-500 bg-red-50 hover:bg-red-100 rounded-xl transition-colors"
              title="Remove interest"
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
