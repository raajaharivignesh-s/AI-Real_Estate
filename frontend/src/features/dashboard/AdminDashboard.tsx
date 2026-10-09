import { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthContext';
import { Building2, Users, LifeBuoy, CreditCard } from 'lucide-react';

export const AdminDashboard = () => {
  const { user, logout } = useAuth();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch('http://localhost:8000/api/v1/admin/analytics/summary', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          setData(await res.json());
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="p-8 text-center text-slate-600">Loading admin data...</div>;
  if (user?.role !== 'admin') return <div className="p-8 text-center text-red-600">Unauthorized</div>;

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8 bg-slate-900 text-white p-6 rounded-xl shadow-lg">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            Admin Command Center
            <span className="bg-red-500 text-white text-xs px-2 py-1 rounded-full font-bold uppercase tracking-wider">Admin</span>
          </h1>
          <p className="text-slate-300 mt-2">Welcome back, {user.full_name}</p>
        </div>
        <div className="flex gap-4 items-center">
          <a href="/properties" className="text-slate-300 hover:text-white transition">View Site</a>
          <button onClick={logout} className="bg-slate-700 text-white px-4 py-2 rounded hover:bg-slate-600 transition">Logout</button>
        </div>
      </div>

      {data && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="bg-indigo-100 p-4 rounded-full text-indigo-600"><Building2 size={24} /></div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Total Properties</p>
              <p className="text-2xl font-bold text-slate-800">{data.properties.total}</p>
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="bg-emerald-100 p-4 rounded-full text-emerald-600"><Users size={24} /></div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Total Customers</p>
              <p className="text-2xl font-bold text-slate-800">{data.users.total_customers}</p>
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="bg-amber-100 p-4 rounded-full text-amber-600"><LifeBuoy size={24} /></div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Support Tickets</p>
              <p className="text-2xl font-bold text-slate-800">{data.support.total}</p>
            </div>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 flex items-center gap-4">
            <div className="bg-blue-100 p-4 rounded-full text-blue-600"><CreditCard size={24} /></div>
            <div>
              <p className="text-sm text-slate-500 font-medium">Total Bookings</p>
              <p className="text-2xl font-bold text-slate-800">{data.bookings.total}</p>
            </div>
          </div>
        </div>
      )}
      
      <div className="bg-white p-8 rounded-xl shadow border border-slate-200">
        <h2 className="text-xl font-bold text-slate-800 mb-4">Site Visits Breakdown</h2>
        {data && (
          <div className="flex gap-4 flex-wrap">
            {Object.entries(data.visits.by_status).map(([status, count]: [string, any]) => (
              <div key={status} className="bg-slate-50 px-4 py-3 rounded-lg border border-slate-100 text-center min-w-[120px]">
                <p className="text-xl font-bold text-slate-700">{count}</p>
                <p className="text-xs text-slate-500 uppercase tracking-wider mt-1">{status}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
