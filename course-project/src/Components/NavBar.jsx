
// NavBar component to display the navigation bar
export default function NavBar() {
    return (
        // nav bar, will add links and stuff with react router later
        <nav className="flex p-4 bg-blue-500 justify-left">
            <div className="p-2 text-2xl text-white">Course Recommender</div>
            <div className="p-2 text-2xl text-white">Login</div>
            <div className="p-2 text-2xl text-white">Search</div>
        </nav>
    );
} 