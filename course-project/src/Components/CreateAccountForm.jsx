import { useForm } from "react-hook-form";
import useApiPost from "../hooks/useApiPost";
import { SetCookie } from "./CookieUtils";

export default function CreateAccountForm({ setDisplayLoginPage, toggleForm }) {
  const { register, handleSubmit } = useForm();

  const { execute: postRegister } = useApiPost({ api: "/api/register" });

  const onSubmit = async (data) => {
    try {
      console.log("Registration data: ", data);
      if (data.username.trim() === "" || data.password.trim() === "") {
        alert("Please enter a username and password");
        return;
      }
      const response = await postRegister(data);
      console.log("Server response:", response);
      if (response && response.status === "ok" && response.data) {
        // Sets a cookie in the frontend
        SetCookie("username", response.data.username, 3600);
        setDisplayLoginPage(false);
      } else if (response && response.status === "error") {
        alert(response.message || "Registration failed");
      }
    } catch (error) {
      if (error.response?.status === 400) {
        alert("Username already exists.");
      } else {
        console.error(
          "An unexpected error occurred during registration:",
          error,
        );
        alert("Failed to register. Please try again.");
      }
    }
  };

  return (
    <div className="flex flex-col items-center bg-white">
      <div className="flex flex-col items-center w-full">
        <h2 className="text-3xl font-extrabold text-slate-900 mb-2">
          Create Account
        </h2>
        <p className="text-slate-500 mb-8 text-center">
          Choose a unique user ID to get started
        </p>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col w-full gap-4"
        >
          <input
            {...register("username")}
            placeholder="Unique User ID"
            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-400"
          />
          <input
            {...register("password")}
            type="password"
            placeholder="Password"
            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-400"
          />
          <div className="flex flex-col sm:flex-row gap-3 mt-2">
            <button
              type="button"
              onClick={toggleForm}
              className="w-full sm:w-1/2 bg-slate-100 text-slate-700 py-3 px-6 rounded-xl font-semibold hover:bg-slate-200 transition-colors cursor-pointer"
            >
              Back to Login
            </button>
            <button
              type="submit"
              className="w-full sm:w-1/2 bg-indigo-600 text-white py-3 px-6 rounded-xl font-semibold shadow-sm hover:bg-indigo-700 hover:shadow transition-all cursor-pointer"
            >
              Register
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
