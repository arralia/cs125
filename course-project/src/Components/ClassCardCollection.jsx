import Card from "./Card";
import useApiGet from "./useApiGet";
import { useEffect } from "react";
import ReadCookie from "./ReadCookie";

export default function ClassCardCollection() {
  // Handle the cookie logic cleanly
  const userId = ReadCookie("user_id") || null;

  // Destructure the values from your hook
  const {
    execute,
    loading,
    response: classes,
  } = useApiGet({
    api: "/api/classInfo",
  });

  // Use useEffect to trigger the fetch once
  useEffect(() => {
    execute({ params: { userid: userId } });
    // We pass an empty array [] below so this only runs ONCE on mount
  }, []);

  return (
    <div className="flex flex-col justify-center p-4 gap-4">
      {classes?.data?.map((item, index) => (
        <Card
          key={index} // Keys help React track list items
          className={item.className}
          description={item.description}
        />
      ))}
    </div>
  );
}
