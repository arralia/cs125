import NavBar from "./components/NavBar";
import UserSettingsPage from "./pages/UserSettingsPage";
import LoginPage from "./pages/LoginPage";
import { useState } from "react";
import CoursesPage from "./pages/CoursesPage";
import RecommendedCoursesPage from "./pages/RecommendedCoursesPage";

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
