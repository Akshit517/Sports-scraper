import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white p-4 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-red-500">GCTech-Web</Link>
        <div className="flex space-x-6">
          <Link to="/" className="hover:text-red-400">Home</Link>
          <Link to="/cricket" className="hover:text-red-400">Cricket</Link>
          <Link to="/football" className="hover:text-red-400">Football</Link>
          <Link to="/about" className="hover:text-red-400">About</Link>
        </div>
      </div>
    </nav>
  );
}