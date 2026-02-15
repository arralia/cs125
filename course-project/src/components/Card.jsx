// Card class to display class information
export default function Card({ className, description }) {
  // just a null check to see if the data is loaded yet
  // if it is null, it will display "Loading..."
  if (className === null || description === null) {
    className = "Loading...";
    description = "Loading...";
  }

  return (
    <div className="flex flex-col justify-center bg-blue-300 rounded-lg shadow-md max-w-sm transition-all hover:shadow-lg  hover:scale-101">
      <div className="text-lg text-white p-2 text-center bg-blue-400 rounded-t-lg">
        {className}
      </div>
      <div className="text-lg text-white p-4 rounded-b-lg">{description}</div>
    </div>
  );
}
