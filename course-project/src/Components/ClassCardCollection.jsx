import Card from "./Card";
import useApiGet from "./useApiGet";

export default function ClassCardCollection() {
  const classes = useApiGet({ api: "/api/classInfo" });

  return (
    <div className="flex justify-left p-4 gap-4">
      <Card
        className={classes?.data?.[0]?.className} //the ? is a null check
        description={classes?.data?.[0]?.description}
      />
      <Card
        className={classes?.data?.[1]?.className}
        description={classes?.data?.[1]?.description}
      />
      <Card
        className={classes?.data?.[2]?.className}
        description={classes?.data?.[2]?.description}
      />
    </div>
  );
}
