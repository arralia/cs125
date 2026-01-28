import { useState } from "react";

// Form: the stuff needed
// name, selected lists of classes taken and the difficulty of each class,
// list of skills and their difficultys, selection for CS specialization
// Quarters left till graditiaton

import { useForm } from "react-hook-form";

export default function UserInfoForm() {
  // These are the 3 tools you'll use 90% of the time
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => {
    console.log("Clean JSON data:", data);
  };

  return (
    <div>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input {...register("name")} />
        <input {...register("email")} />
        <input type="submit" /> 
      </form>
    </div>
  );
}
