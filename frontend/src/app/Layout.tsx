import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../features/auth/AuthContext';
import { Building2, LogOut } from 'lucide-react';

export const Layout = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isAuthPage = location.pathname === '/login' || location.pathname === '/register';

  if (isAuthPage) return <Outlet />;

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <header className="sticky top-0 z-40 glass border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 md:px-8 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-xl font-bold text-slate-800 hover:opacity-80 transition">
            <div className="p-1.5 premium-gradient text-white rounded-lg shadow-sm"><Building2 size={20} /></div>
            AI - <span className="text-teal-600">Real Estate</span>
          </Link>
          
          <nav className="hidden md:flex items-center gap-8 font-medium text-slate-600 text-sm">
            <Link to="/properties" className={`hover:text-teal-600 transition ${location.pathname.includes('/properties') ? 'text-teal-600 font-bold' : ''}`}>Explore Properties</Link>
            {user && <Link to="/wishlist" className={`hover:text-teal-600 transition ${location.pathname === '/wishlist' ? 'text-teal-600 font-bold' : ''}`}>My Wishlist</Link>}
            {user && <Link to="/dashboard" className={`hover:text-teal-600 transition ${location.pathname === '/dashboard' ? 'text-teal-600 font-bold' : ''}`}>Dashboard</Link>}
          </nav>

          <div className="flex items-center gap-4">
            {!user ? (
              <>
                <Link to="/login" className="text-slate-600 hover:text-teal-600 font-medium text-sm transition hidden sm:block">Sign In</Link>
                <Link to="/register" className="bg-slate-800 text-white px-5 py-2 rounded-full text-sm font-medium hover:bg-slate-700 transition hover-lift">Get Started</Link>
              </>
            ) : (
              <div className="flex items-center gap-4">
                <div className="hidden sm:flex flex-col items-end">
                  <span className="text-sm font-bold text-slate-800 leading-none">{user.full_name}</span>
                  <span className="text-[10px] text-slate-400 uppercase tracking-wider font-bold mt-1">{user.role}</span>
                </div>
                <button onClick={logout} className="p-2 text-slate-400 hover:text-red-500 transition rounded-full hover:bg-red-50" title="Logout">
                  <LogOut size={20} />
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="flex-1 animate-in fade-in duration-300">
        <Outlet />
      </main>

      <footer className="bg-slate-900 text-slate-400 py-12 mt-auto border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 md:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2 text-xl font-bold text-white">
             <Building2 size={24} /> AI - Real Estate
          </div>
          <p className="text-sm">© {new Date().getFullYear()} AI - Real Estate Platform. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};
