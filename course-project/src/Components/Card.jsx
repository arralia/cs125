
export default function Card() {
    return (
        <div className="flex flex-col bg-blue-300 rounded-lg shadow-md max-w-sm m-4">
            <div className="text-lg text-white p-2 text-center bg-blue-400 rounded-t-lg">
                Class Name
            </div>
            <div className="text-lg text-white p-4">
                Class Description:
            </div>
        </div>
    );
}

