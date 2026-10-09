import { createBrowserRouter, Navigate } from 'react-router-dom';
import { LoginForm } from '../features/auth/LoginForm';
import { RegisterForm } from '../features/auth/RegisterForm';
import { useAuth } from '../features/auth/AuthContext';
import { PropertyListPage } from '../features/properties/PropertyListPage';
import { PropertyDetailsPage } from '../features/properties/PropertyDetailsPage';
import { WishlistPage } from '../features/wishlist/WishlistPage';
import { ComparePage } from '../features/properties/ComparePage';
import { Dashboard } from '../features/dashboard/Dashboard';
import { AdminDashboard } from '../features/dashboard/AdminDashboard';
import { Layout } from './Layout';

// Basic Protected Route wrapper
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { user, isLoading } = useAuth();
  if (isLoading) return <div className="p-20 text-center animate-pulse text-teal-600 font-bold">Loading your secure session...</div>;
  if (!user) return <Navigate to="/login" />;
  return <>{children}</>;
};

const RoleBasedDashboard = () => {
  const { user } = useAuth();
  if (user?.role === 'admin') return <AdminDashboard />;
  return <Dashboard />;
};

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Navigate to="/properties" replace />
      },
      {
        path: 'login',
        element: <LoginForm />
      },
      {
        path: 'register',
        element: <RegisterForm />
      },
      {
        path: 'dashboard',
        element: <ProtectedRoute><RoleBasedDashboard /></ProtectedRoute>
      },
      {
        path: 'properties',
        element: <PropertyListPage />
      },
      {
        path: 'properties/:id',
        element: <PropertyDetailsPage />
      },
      {
        path: 'wishlist',
        element: <ProtectedRoute><WishlistPage /></ProtectedRoute>
      },
      {
        path: 'compare',
        element: <ComparePage />
      },
      {
        path: '*',
        element: (
          <div className="p-20 text-center flex flex-col items-center justify-center min-h-[60vh]">
            <h1 className="text-6xl font-bold text-slate-200 mb-4">404</h1>
            <h2 className="text-2xl font-bold text-slate-800 mb-2">Page Not Found</h2>
            <p className="text-slate-500 mb-8">The address you are looking for might have been moved or doesn't exist.</p>
            <a href="/properties" className="bg-teal-600 text-white px-6 py-3 rounded-full font-medium hover:bg-teal-700 transition">Return to Safety</a>
          </div>
        )
      }
    ]
  }
]);
