import Card from "./Card";

export default function ClassCardCollection({ data, className }) {
  return (
    <div className={`grid gap-4 ${className || "grid-cols-1"}`}>
      {data?.map((item, index) => (
        <Card
          key={index} // Keys help React track list items
          className={item.id}
          description={item.title}
        />
      ))}
    </div>
  );
}
