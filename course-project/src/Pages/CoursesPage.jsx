import ClassCardCollection from "../Components/ClassCardCollection";

export default function CoursesPage() {
  return (
    <div className="flex flex-col justify-center items-center bg-blue-100 mx-auto rounded-lg m-4">
      <h1 className="text-2xl font-bold mb-2 p-2 text-white bg-blue-400 rounded-lg px-8 m-2">
        All Courses
      </h1>
      <div className="flex flex-col items-center max-h-[620px] overflow-y-auto pr-2 scrollbar-custom">
        <ClassCardCollection api="/api/allClassesData" />
      </div>
    </div>
  );
}
