import { useForm } from "react-hook-form";
import useApiPost from "../hooks/useApiPost";
import { useEffect, useState } from "react";
import { ReadCookie, SetCookie } from "./CookieUtils";

export default function LoginForm({ setDisplayLoginPage, toggleForm }) {
  const { register, handleSubmit } = useForm();

  const [loggedIn, setLoggedIn] = useState(false);

  const { execute: postLogin } = useApiPost({ api: "/api/login" });

  // this is the onSubmit function for the form
  const onSubmit = async (data) => {
    try {
      console.log("data: ", data);
      if (data.username.trim() === "" || data.password.trim() === "") {
        alert("Please enter a username and password");
        return;
      }
      const response = await postLogin(data);
      console.log("Server response:", response);
      if (response && response.status === "ok" && response.data) {
        // this line here sets a cookie in the frontend
        SetCookie("username", response.data.username, 3600);
        setDisplayLoginPage(false);
      } else if (response && response.status === "error") {
        alert(response.message || "Login failed");
      }
    } catch (error) {
      // Logic for when the user does NOT exist (or other errors)
      if (error.response?.status === 404) {
        alert("This User ID does not exist in our records.");
      } else {
        console.error("An unexpected error occurred:", error);
        alert("An error occurred during login. Please try again.");
      }
    }
  };

  const handleLogout = () => {
    document.cookie = "username=; path=/; max-age=0; SameSite=Lax";
    setLoggedIn(false);
    setDisplayLoginPage(false);
  };

  useEffect(() => {
    // get the cookie for username and see if they exist
    if (document.cookie.includes("username")) {
      setLoggedIn(true);
    } else {
      setLoggedIn(false);
    }
  }, []);

  return (
    <div className="flex flex-col items-center bg-white">
      {loggedIn && (
        <div className="flex flex-col items-center justify-center gap-6 w-full py-4">
          <div className="w-16 h-16 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center mb-2">
            <svg
              xmlns="http://www.w3.org/20兆/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-8 h-8"
            >
              <path
                fillRule="evenodd"
                d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-slate-800">Your Account</h2>
          <div className="flex flex-col gap-4 w-full">
            <div className="bg-slate-50 border border-slate-100 p-4 rounded-xl text-center">
              <p className="text-sm text-slate-500 mb-1">Signed in as</p>
              <p className="text-lg font-bold text-slate-800">
                {ReadCookie("username")}
              </p>
            </div>
            <button
              type="button"
              onClick={handleLogout}
              className="w-full bg-rose-500 text-white py-3 px-6 rounded-xl font-semibold hover:bg-rose-600 shadow-sm transition-colors cursor-pointer"
            >
              Sign Out
            </button>
          </div>
        </div>
      )}
      {!loggedIn && (
        <div className="flex flex-col items-center w-full">
          <h2 className="text-3xl font-extrabold text-slate-900 mb-2">
            Welcome Back
          </h2>
          <p className="text-slate-500 mb-8 text-center">
            Enter your unique user ID to login
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
                Register
              </button>
              <button
                type="submit"
                className="w-full sm:w-1/2 bg-indigo-600 text-white py-3 px-6 rounded-xl font-semibold shadow-sm hover:bg-indigo-700 hover:shadow transition-all cursor-pointer"
              >
                Login
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
