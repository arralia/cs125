import useApiGet from "../hooks/useApiGet";
import { useEffect, useState } from "react";
import ClassCardCollection from "../Components/ClassCardCollection";

export default function CoursesPage() {
  const [classes, setClasses] = useState([]);

  // Destructure the values from your hook
  const { execute } = useApiGet({
    api: "/api/allClassesData",
  });

  // Use useEffect to trigger the fetch once
  useEffect(() => {
    execute().then((res) => {
      setClasses(res?.data);
    });
    //
  }, [execute]);

  return (
    <div className="flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-full">
      <div className="p-6 border-b border-slate-100 bg-slate-50/50">
        <h2 className="text-xl font-bold text-slate-800">All Courses</h2>
        <p className="text-sm text-slate-500 mt-1">Browse the full catalog</p>
      </div>
      <div className="p-6 flex-1 min-h-0 overflow-y-auto scrollbar-custom ">
        <ClassCardCollection data={classes} className="grid-cols-1" />
      </div>
    </div>
  );
}
