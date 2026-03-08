import { cleanCourseName } from "../Util/Util";

// Card class to display class information
export default function Card({ className, description, index }) {
  // just a null check to see if the data is loaded yet
  // if it is null, it will display "Loading..."
  if (className === null || description === null) {
    className = "Loading...";
    description = "Loading...";
  }

  return (
    <div className="group flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 hover:shadow-lg hover:-translate-y-1 hover:border-indigo-300 transition-all duration-300 cursor-pointer overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/80 group-hover:bg-indigo-50/80 transition-colors">
        <div className="flex items-center gap-3">
          {index !== undefined && (
            <div className="rounded-full min-w-[28px] h-7 flex items-center justify-center shrink-0 shadow-inner bg-slate-200 text-slate-600 group-hover:bg-indigo-600 group-hover:text-white transition-all text-xs font-bold">
              {index + 1}
            </div>
          )}
          <h3 className="text-lg font-bold text-slate-800 tracking-tight">
            {cleanCourseName(className)}
          </h3>
        </div>
      </div>
      <div className="p-5 flex-1 bg-white">
        <p className="text-slate-600 leading-relaxed text-sm">{description}</p>
      </div>
    </div>
  );
}
