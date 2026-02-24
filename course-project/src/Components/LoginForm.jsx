import { useForm } from "react-hook-form";
import useApiPost from "../hooks/useApiPost";
import { useEffect, useState } from "react";
import ReadCookie from "./CookieUtils";

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
        document.cookie = `username=${response.data.username}; path=/; max-age=3600; SameSite=Lax`;
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
        <div className="flex items-center flex-col justify-center items-center gap-4">
          <h2 className="text-2xl font-bold mb-2">Account</h2>
          <div className="flex flex-row gap-4">
            <p className="text-md font-bold bg-gray-200 p-2 rounded-md">
              Logged in as: {ReadCookie("username")}
            </p>
            <button
              type="button"
              onClick={handleLogout}
              className="bg-red-500 text-white py-2 px-6 rounded-md hover:bg-red-600 cursor-pointer"
            >
              Logout
            </button>
          </div>
        </div>
      )}
      {!loggedIn && (
        <div className="flex flex-col items-center">
          <h2 className="text-2xl font-bold mb-2">Login</h2>
          <p className="text-gray-600 mb-8">
            Enter your unique user ID to login
          </p>

          <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col items-center gap-4"
          >
            <input
              {...register("username")}
              placeholder="Unique User ID"
              className="border border-gray-300 rounded-md py-2 px-4 hover:border-blue-500"
            />
            <input
              {...register("password")}
              type="password"
              placeholder="Password"
              className="border border-gray-300 rounded-md py-2 px-4 hover:border-blue-500"
            />
            <div className="flex flex-row gap-4">
             
              <button
                type="button"
                onClick={toggleForm}
                className="bg-green-500 text-white py-2 px-6 rounded-md hover:bg-green-600 cursor-pointer"
              >
                Register
              </button>
               <button
                type="submit"
                className="bg-blue-500 text-white py-2 px-6 rounded-md hover:bg-blue-600 cursor-pointer"
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
