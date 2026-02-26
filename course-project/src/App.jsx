import NavBar from "./components/NavBar";
import UserSettingsPage from "./Pages/UserSettingsPage";
import LoginPage from "./Pages/LoginPage";
import { useState } from "react";
import CoursesPage from "./Pages/CoursesPage";
import RecommendedCoursesPage from "./Pages/RecommendedCoursesPage";

function App() {
  const [loginPrompt, setLogin] = useState(false);
  const [settingsPrompt, setSettings] = useState(false);

  return (
    <div className="flex flex-col h-screen">
      <NavBar setLogin={setLogin} setSettings={setSettings} />
      {loginPrompt ? <LoginPage setLogin={setLogin} /> : null}
      {settingsPrompt ? <UserSettingsPage setSettings={setSettings} /> : null}

      <div className="flex justify-right items-center ">
        <RecommendedCoursesPage />
        <CoursesPage />
      </div>
    </div>
  );
}

export default App;
