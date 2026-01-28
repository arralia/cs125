import LoginForm from "../Components/LoginForm";

export default function LoginPage({setLogin}) {
    return (
        <div className="fixed inset-0 flex justify-center items-center bg-black/40 backdrop-blur-sm z-50 p-4">
            <div className="flex flex-col justify-left z-50 max-w-md mx-auto bg-white p-10 rounded-lg">
                <h2 className="text-2xl font-bold mb-2">Login</h2>
                <p className="text-gray-600 mb-8">Enter your unique user ID to login</p>
                <LoginForm setLogin={setLogin} />
            </div>
        </div>
    );
}