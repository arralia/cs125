import NavBar from "./Components/NavBar";
import UserSettingsPage from "./Pages/UserSettingsPage";
import LoginPage from "./Pages/LoginPage";
import { useState } from "react";
import CoursesPage from "./Pages/CoursesPage";
import RecommendedCoursesPage from "./Pages/RecommendedCoursesPage";

function App() {
  const [displayLoginPage, setDisplayLoginPage] = useState(false);
  const [displaySettingsPage, setDisplaySettingsPage] = useState(false);

  return (
    <div className="flex flex-col h-screen">
      <NavBar
        setDisplayLoginPage={setDisplayLoginPage}
        setDisplaySettingsPage={setDisplaySettingsPage}
      />
      {displayLoginPage ? (
        <LoginPage setDisplayLoginPage={setDisplayLoginPage} />
      ) : null}
      {displaySettingsPage ? (
        <UserSettingsPage setDisplaySettingsPage={setDisplaySettingsPage} />
      ) : null}

      <div className="flex justify-right items-center ">
        <RecommendedCoursesPage />
        <CoursesPage />
      </div>
    </div>
  );
}

export default App;
