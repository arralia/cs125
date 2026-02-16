import { useForm } from "react-hook-form";
import useApiPost from "../hooks/useApiPost";
import { useEffect, useState } from "react";
import ReadCookie from "./ReadCookie";

export default function LoginForm({ setLogin }) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const [loggedIn, setLoggedIn] = useState(false);

  const { execute: postLogin, loading } = useApiPost({ api: "/api/login" });

  // this is the onSubmit function for the form
  const onSubmit = async (data) => {
    try {
      const response = await postLogin(data);
      console.log("Server response:", response.data);
      if (response) {
        // this line here sets a cookie in the frontend
        document.cookie = `username=${response.data.username}; path=/; max-age=3600; SameSite=Lax`;
        setLogin(false);
      }
    } catch (error) {
      // Logic for when the user does NOT exist (or other errors)
      if (error.response?.status === 404) {
        alert("This User ID does not exist in our records.");
      } else {
        console.error("An unexpected error occurred:", error);
      }
    }
  };

  useEffect(() => {
    // get the cookie for username and see if htye exist, if they do
    if (document.cookie.includes("username")) {
      setLoggedIn(true);
      const username = ReadCookie("username");
    } else {
      setLoggedIn(false);
    }
  }, []);

  return (
    <div className="flex flex-col items-center bg-white">
      {loggedIn && (
        <p className="text-md font-bold mb-6 bg-gray-200 p-2 rounded-md">
          Logged in as: {ReadCookie("username")}
        </p>
      )}
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex items-center gap-4"
      >
        <input
          {...register("username")}
          placeholder="Unique User ID"
          className="border border-gray-300 rounded-md py-2 px-4 hover:border-blue-500"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white py-2 px-6 rounded-md hover:bg-blue-600 cursor-pointer"
        >
          Login
        </button>
      </form>
    </div>
  );
}
