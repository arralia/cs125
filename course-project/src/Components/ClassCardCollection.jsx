import Card from "./Card";
import useApiGet from "./useApiGet";
import readCookie from "./readCookie";
import { useEffect } from "react";

export default function ClassCardCollection() {
  // Handle the cookie logic cleanly
  const userId = readCookie("user_id") || null;

  // Destructure the values from your hook
  const { execute, loading, response : classes} = useApiGet({
    api: "/api/classInfo"
  });

  // Use useEffect to trigger the fetch once
  useEffect(() => {
    execute({ params: { userid: userId } }); 
    // We pass an empty array [] below so this only runs ONCE on mount
  }, []);

  return (
    <div className="flex justify-left p-4 gap-4">
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