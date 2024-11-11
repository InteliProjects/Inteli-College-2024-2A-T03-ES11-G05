import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { Manager } from './pages/Manager/Manager'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { TopSalesMans } from './pages/Manager/TopSalesMan';
import { ProductAndCategori } from './pages/Manager/ProductAndCategori';
import { SalesMan } from './pages/Salesman/salesman';
import { Dashboard } from './pages/Salesman/dashboard';
import { Login_start } from './pages/Login_start';
import { Login } from './pages/Login';
import { Toaster } from '@/components/ui/toaster'


const router = createBrowserRouter([
  {
    path: "/",
    element: <Login_start />
  },
  {
    path: "/login",
    element: <Login />
  },
  {
    path: "/manager",
    element: <Manager />,
  },
  {
    path: "/manager/topSalesMan",
    element: <TopSalesMans />
  },
  {
    path: "/manager/productAndCategori",
    element: <ProductAndCategori />
  },
  {
    path: "/salesMan",
    element: <SalesMan />
  },
  {
    path: "/dash",
    element: <Dashboard />
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Toaster />
    <RouterProvider router={router} />
  </StrictMode >,
)
