

//Card class to display class information
export default function Card({className, description}) {
    return (
        <div className="flex flex-col bg-blue-300 rounded-lg shadow-md max-w-sm m-4">
            <div className="text-lg text-white p-2 text-center bg-blue-400 rounded-t-lg">
                {className}
            </div>
            <div className="text-lg text-white p-4 rounded-b-lg">
                {description}
            </div>
        </div>
    );
}

