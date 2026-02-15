// NavBar component to display the navigation bar

import { CircleUserRound, LibraryBig, Settings } from "lucide-react";
import SearchBar from "./SearchBar";

export default function NavBar({ setLogin, setSettings }) {
  return (
    // nav bar, will add links and stuff with react router later
    <nav className="flex p-4 bg-blue-500 items-center justify-between">
      <div className="flex items-center">
        <LibraryBig className="size-10 text-white" />
        <div className="p-2 text-2xl text-white cursor-default">
          Course Recommender
        </div>
        <SearchBar />
      </div>
      <div className="flex items-center pr-4 gap-4 text-white cursor-pointer">
        <Settings className="size-8" onClick={() => setSettings(true)} />
        <CircleUserRound className="size-8" onClick={() => setLogin(true)} />
      </div>
    </nav>
  );
}
