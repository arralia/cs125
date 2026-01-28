import { useForm } from "react-hook-form";
import useApiPost from "./useApiPost";

export default function UserInformationForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const { execute: postUserSetInfo, loading } = useApiPost({ api: "/api/userSetInfo" });

  // this is the onSubmit function for the form
  const onSubmit = async (data) => {
    try {
      const response = await postUserSetInfo(data);
      console.log("Server response:", response);
      if (response) {
        console.log("User Set Info successful!");
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
