import Card from "./Card";
import useApiGet from "./useApiGet";
import { useEffect } from "react";
import ReadCookie from "./readCookie";

export default function ClassCardCollection({ api }) {
  // Handle the cookie logic cleanly
  const userId = ReadCookie("user_id") || null;

  // Destructure the values from your hook
  const {
    execute,
    loading,
    response: classes,
  } = useApiGet({
    api: api,
  });

  // Use useEffect to trigger the fetch once
  useEffect(() => {
    console.log("calling api" + api);
    execute({ params: { userid: userId } });
    console.log(classes);
    // We pass an empty array [] below so this only runs ONCE on mount
  }, []);

  return (
    <div className="flex flex-col p-4 gap-4">
      {classes?.data?.map((item, index) => (
        <Card
          key={index} // Keys help React track list items
          className={item.id}
          description={item.title}
        />
      ))}
    </div>
  );
}
