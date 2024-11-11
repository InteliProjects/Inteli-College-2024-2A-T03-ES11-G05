import { Menu, User, ShoppingBag, UserSearch } from "lucide-react";
import { Link } from "react-router-dom";

export function Sidebar({ toggleSidebar, isOpen, userRoute, salesManRoute, isManagerPage }) {
  return (
    <div
      className={`fixed top-0 left-0 h-screen w-16 bg-black z-[9999] flex flex-col items-center py-8 space-y-6 transition-transform duration-300 ${
        isOpen ? "translate-x-0" : "-translate-x-full"
      }`}
    >
      <button
        className="text-black border border-white bg-white rounded-xl p-2"
        onClick={toggleSidebar}
      >
        <Menu size={24} />
      </button>

      <Link to={userRoute}>
        <button className="text-white border border-white bg-slate-500 rounded-xl p-2">
          <User size={24} />
        </button>
      </Link>

      <Link to={salesManRoute}>
        <button className="text-white border border-white bg-slate-500 rounded-xl p-2">
          <ShoppingBag size={24} />
        </button>
      </Link>

      {/* ícone extra página de Manager */}
      {isManagerPage && (
        <Link to="/manager/topSalesMan">
          <button className="text-white border border-white bg-slate-500 rounded-xl p-2">
            <UserSearch size={24} />
          </button>
        </Link>
      )}
    </div>
  );
}