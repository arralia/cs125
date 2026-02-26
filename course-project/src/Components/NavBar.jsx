// NavBar component to display the navigation bar

import { CircleUserRound, LibraryBig, Settings } from "lucide-react";
import SearchBar from "./SearchBar";

export default function NavBar({
  setDisplayLoginPage,
  setDisplaySettingsPage,
}) {
  return (
    <nav className="sticky top-0 z-40 w-full bg-white/80 backdrop-blur-md border-b border-slate-200 shadow-sm transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center gap-3">
            <div className="bg-indigo-600 p-2 rounded-xl text-white shadow-md shadow-indigo-200">
              <LibraryBig className="size-6" />
            </div>
            <div className="text-xl font-bold text-slate-800 tracking-tight cursor-default">
              Course Recommender
            </div>
          </div>

          <div className="hidden md:block flex-1 max-w-md mx-8">
            <SearchBar />
          </div>

          <div className="flex items-center gap-4 text-slate-500">
            <button
              onClick={() => setDisplaySettingsPage(true)}
              className="p-2 hover:bg-slate-100 hover:text-indigo-600 rounded-full transition-colors cursor-pointer"
              aria-label="Settings"
            >
              <Settings className="size-6" />
            </button>
            <button
              onClick={() => setDisplayLoginPage(true)}
              className="p-2 hover:bg-slate-100 hover:text-indigo-600 rounded-full transition-colors cursor-pointer"
              aria-label="Account"
            >
              <CircleUserRound className="size-6" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
