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
    <div className="flex flex-col h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
      <NavBar
        setDisplayLoginPage={setDisplayLoginPage}
        setDisplaySettingsPage={setDisplaySettingsPage}
      />
      {displayLoginPage && (
        <LoginPage setDisplayLoginPage={setDisplayLoginPage} />
      )}
      {displaySettingsPage && (
        <UserSettingsPage setDisplaySettingsPage={setDisplaySettingsPage} />
      )}

      {/* Main Dashboard Layout */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8 flex flex-col min-h-0">
        <div className="mb-6 shrink-0">
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Your Dashboard
          </h1>
          <p className="mt-1 text-lg text-slate-600">
            Discover and plan your upcoming courses based on your interests.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start flex-1 min-h-0 pb-4">
          {/* Main Content Area: Recommended Courses */}
          <div className="lg:col-span-3 h-full flex flex-col min-h-0">
            <RecommendedCoursesPage />
          </div>

          {/* Sidebar Area: All Courses */}
          <div className="lg:col-span-2 h-full flex flex-col min-h-0">
            <CoursesPage />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
