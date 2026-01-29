// Form: the stuff needed
// name, selected lists of classes taken and the difficulty of each class,
// list of skills and their difficultys, selection for CS specialization
// Quarters left till graditiaton

import { useForm } from "react-hook-form";

export default function UserSettingsForm() {
  // These are the 3 tools you'll use 90% of the time
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => {
    console.log("Clean JSON data:", data);
  };

  const skills = [
    { name: "Math", value: 0 },
    { name: "Physics", value: 0 },
    { name: "Chemistry", value: 0 },
    { name: "Biology", value: 0 },
    { name: "Computer Science", value: 0 },
  ];



  return (
    <div>
      <h2 className="text-3xl font-bold mb-2">User Settings</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <h3 className="text-xl font-bold">Skills</h3> 
        {/* map through the skills */}
        {skills.map((skill) => (
          <div className="flex gap-4 justify-between">
            <label>{skill.name}</label>
            <div className="flex gap-2 justify-center items-center">
              <label>1</label>
                  <input id={skill.name} type="range"min="1" max="5" step="1" {...register(skill.name)} />
              <label>5</label>
            </div>
          </div>
        ))}
        <input type="submit" value="Save" className="bg-blue-500 text-white py-2 px-6 rounded-md hover:bg-blue-600 cursor-pointer" />
      </form>
    </div>
  );
}
