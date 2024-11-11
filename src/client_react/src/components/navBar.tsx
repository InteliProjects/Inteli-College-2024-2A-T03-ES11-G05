import { useState } from "react";
import { AlignJustify } from "lucide-react";
import { Sidebar } from "../components/sideBar";
import { SearchToggle } from "../components/searchToggle";

export function NavBar({ userRoute, salesManRoute, isManagerPage }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <nav className="flex justify-between items-center mb-7">
      <button className="text-xl" onClick={toggleSidebar}>
        <AlignJustify />
      </button>

      <button className="text-xl ml-3">
        <SearchToggle />
      </button>

      <Sidebar
        toggleSidebar={toggleSidebar}
        isOpen={isSidebarOpen}
        userRoute={userRoute}
        salesManRoute={salesManRoute}
        isManagerPage={isManagerPage} // Passando a prop para a Sidebar
      />

    </nav>
  );
}
