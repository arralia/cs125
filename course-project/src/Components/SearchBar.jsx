import { Search } from "lucide-react";

export default function SearchBar() {
  // Search bar tailwind created by gemini ai
  return (
    <div className="flex items-center bg-white rounded-full px-4 py-1 w-80">
      <Search className="size-5 text-gray-400 mr-2" />
      <input
        type="text"
        placeholder="Search..."
        className="outline-none w-full text-sm"
      />
    </div>
  );
}
