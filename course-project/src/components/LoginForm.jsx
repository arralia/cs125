import { useForm } from "react-hook-form";
import useApiPost from "../hooks/useApiPost";

export default function LoginForm({ setLogin }) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const { execute: postLogin, loading } = useApiPost({ api: "/api/login" });

  // this is the onSubmit function for the form
  const onSubmit = async (data) => {
    try {
      const response = await postLogin(data);
      console.log("Server response:", response.data);
      if (response) {
        // this line here sets a cookie in the frontend
<<<<<<< HEAD:course-project/src/components/LoginForm.jsx
        document.cookie = `username=${response.data.username}; path=/; max-age=3600; SameSite=Lax`;
=======
        document.cookie = `user_id=${response.userid}; path=/; max-age=3600; SameSite=Lax`;
>>>>>>> 59a8f13 (refactor: Relocate API hooks to a dedicated directory, update components for new data fetching patterns, and connected the all classes api to display in the user settings and the homepage):course-project/src/Components/LoginForm.jsx
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
  // todo: put logic for checking if the user exists in the database

  return (
    <div className="flex flex-col items-center bg-white">
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
