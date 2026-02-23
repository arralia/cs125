import useApiGet from "../hooks/useApiGet";
import { useEffect, useState } from "react";
import ClassCardCollection from "../components/ClassCardCollection";

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
    // We pass an empty array [] below so this only runs ONCE on mount
  }, [execute]);

  return (
    <div className="flex flex-col justify-center items-center bg-blue-100 max-w-sm w-full mx-auto rounded-lg m-4">
      <h1 className="text-2xl font-bold mb-2 p-2 text-white bg-blue-400 rounded-lg px-8 m-2">
        All Courses
      </h1>
      <div className="flex flex-col items-center max-h-[620px] overflow-y-auto pr-2 scrollbar-custom bg-black/10 rounded-lg m-2">
        <ClassCardCollection data={classes} />
      </div>
    </div>
  );
}
