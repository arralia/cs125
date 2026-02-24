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
      <div className="flex flex-col items-center">
        <h2 className="text-2xl font-bold mb-2">Register</h2>
        <p className="text-gray-600 mb-8">
          Create a unique user ID to get started
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
              className="bg-gray-500 text-white py-2 px-6 rounded-md hover:bg-gray-600 cursor-pointer"
            >
              Back to Login
            </button>
            <button
              type="submit"
              className="bg-green-500 text-white py-2 px-6 rounded-md hover:bg-green-600 cursor-pointer"
            >
              Register
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
