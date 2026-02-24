import { useState, useEffect, useCallback } from "react";
import useApiGet from "../hooks/useApiGet";
import ClassCardCollection from "../Components/ClassCardCollection";
import ReadCookie from "../Components/ReadCookie";

export default function RecommendedCoursesPage() {
  const [recommendedClasses, setRecommendedClasses] = useState([]);
  const [username, setUsername] = useState(() => ReadCookie("username") || "");

  const { execute } = useApiGet({
    api: "/api/recommendedClasses",
  });
  // TODO: better way to make sure recommended classes re-render than interval polling...
  const getRecommendedClasses = useCallback(
    (nextUsername) => {
      execute({ params: { username: nextUsername || "" } }).then((res) => {
        setRecommendedClasses(res.data);
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
    getRecommendedClasses(username);
  }, [getRecommendedClasses, username]);

  return (
    <div className="flex flex-col justify-center items-center bg-blue-100 max-w-sm w-full mx-auto rounded-lg m-4">
      <button
        onClick={() => getRecommendedClasses(username)}
        className="text-2xl font-bold mb-2 p-2 text-white bg-blue-400 rounded-lg px-8 m-2 transition-all duration-300 hover:bg-blue-500 hover:scale-101 active:scale-98 hover:shadow-lg cursor-pointer"
      >
        Recommended Courses
      </button>
      <div className="flex flex-col items-center max-h-[620px] overflow-y-auto pr-2 scrollbar-custom bg-black/10 rounded-lg m-2">
        <ClassCardCollection data={recommendedClasses} />
      </div>
    </div>
  );
}
