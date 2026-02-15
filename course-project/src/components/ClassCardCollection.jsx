import Card from "./Card";

export default function ClassCardCollection({ data }) {
  return (
    <div className="flex flex-col p-4 gap-4">
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
