import { cleanCourseName } from "../Util/Util";

// Card class to display class information
export default function Card({
  className,
  description,
  informalDescription,
  index,
  gpa,
}) {
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
          <h3 className="px-4 py-1.5 bg-white border border-slate-200 rounded-xl text-indigo-600 font-bold text-base tracking-tight whitespace-nowrap shrink-0 transition-all group-hover:border-indigo-300 group-hover:bg-indigo-50/50">
            {cleanCourseName(className)}
          </h3>
          <p className="text-sm text-slate-600">{description}</p>
          {/* <div className="flex flex-col items-end shrink-0 ml-auto">
            <span className="text-[10px]  font-bold text-indigo-600 uppercase leading-none">
              GPA
            </span>
            <span className="text-sm font-bold text-slate-700">
              {gpa ? gpa.toFixed(2) : "N/A"}
            </span>
          </div> */}
        </div>
      </div>
      <div className="p-5 flex-1 bg-white">
        <p className="text-slate-600 leading-relaxed text-sm">
          {informalDescription}
        </p>
      </div>
    </div>
  );
}
