// Form: the stuff needed
// name, selected lists of classes taken and the difficulty of each class,
// list of skills and their difficultys, selection for CS specialization
// Quarters left till graditiaton

import { useForm } from "react-hook-form";
import { useEffect, useState } from "react";
import useApiPost from "./useApiPost";
import useApiGet from "./useApiGet";

export default function UserSettingsForm({ setSettings }) {
  // These are the 3 tools you'll use 90% of the time
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = (data) => {
    setSettings(false);
    console.log("Clean JSON data:", data);
  };

  const [settingsPage, setSettingsPage] = useState("skills");

  // this gets the class info when the settings page first comes up
  // so we can populate the drop down menu for the user to select
  const { execute } = useApiGet({
    api: "/api/classInfo",
  });

  useEffect(() => {
    const classList = execute();
  }, []);

  const skills = [
    { name: "Math", value: 0 },
    { name: "Algorithms", value: 0 },
    { name: "Data Structures", value: 0 },
    { name: "Programming", value: 0 },
    { name: "Recursion", value: 0 },
  ];

  return (
    <div>
      <h2 className="text-3xl font-bold mb-2">User Settings</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
        <div className="flex">
          <button className="text-xl font-bold outline px-3 rounded-l-md hover:text-blue-700 hover:" onClick={() => {setSettingsPage("Skills")}}>
            Skills
          </button>
          <button className="text-xl font-bold outline px-3 rounded-r-md hover:text-blue-700" onClick={() => {setSettingsPage("Classes")}}>
            Classes
          </button>
        </div>
        {/* map through the skills */}
        {skills.map((skill) => (
          <div key={skill.name} className="flex gap-4 justify-between">
            <label>{skill.name}</label>
            <div className="flex gap-2 justify-center items-center">
              <label>1</label>
              <input
                id={skill.name}
                type="range"
                min="1"
                max="5"
                step="1"
                {...register(skill.name)}
              />
              <label>5</label>
            </div>
          </div>
        ))}
        <input
          type="submit"
          value="Save"
          className="bg-blue-500 text-white py-2 px-6 rounded-md hover:bg-blue-600 cursor-pointer"
        />
      </form>
    </div>
  );
}
