import { useState, useEffect } from 'react';
import { useAuth } from '../auth/AuthContext';
import { getVisits, getBookings, getSupportRequests } from '../../api/operations';

export const Dashboard = () => {
  const { user, logout } = useAuth();
  const [visits, setVisits] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [support, setSupport] = useState([]);

  useEffect(() => {
    getVisits().then(setVisits).catch(console.error);
    getBookings().then(setBookings).catch(console.error);
    getSupportRequests().then(setSupport).catch(console.error);
  }, []);

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-8 bg-white p-6 rounded-xl shadow-sm border border-slate-100">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Welcome, {user?.full_name}</h1>
          <p className="text-slate-500 font-medium capitalize mt-1">Role: {user?.role}</p>
        </div>
        <div className="flex gap-4 items-center">
          <a href="/properties" className="text-teal-600 font-medium hover:underline">Browse Properties</a>
          <a href="/wishlist" className="text-teal-600 font-medium hover:underline">My Wishlist</a>
          <button onClick={logout} className="bg-red-50 text-red-600 font-medium px-4 py-2 rounded hover:bg-red-100 transition">Logout</button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-md border-t-4 border-teal-500">
          <h2 className="text-xl font-bold text-slate-800 mb-4 flex items-center justify-between">
            My Visits 
            <span className="bg-teal-100 text-teal-800 text-sm py-1 px-3 rounded-full">{visits.length}</span>
          </h2>
          {visits.length === 0 ? <p className="text-slate-500">No upcoming visits.</p> : visits.map((v: any) => (
            <div key={v.id} className="mb-3 p-4 bg-slate-50 rounded-lg border border-slate-100">
              <p className="font-bold text-slate-700">Property #{v.property_id}</p>
              <p className="text-sm text-slate-500 mb-2">{new Date(v.scheduled_at).toLocaleDateString()} at {new Date(v.scheduled_at).toLocaleTimeString()}</p>
              <span className="text-xs bg-teal-100 text-teal-800 px-2 py-1 rounded capitalize font-medium">{v.status.replace('_', ' ')}</span>
            </div>
          ))}
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-md border-t-4 border-blue-500">
          <h2 className="text-xl font-bold text-slate-800 mb-4 flex items-center justify-between">
            My Bookings
            <span className="bg-blue-100 text-blue-800 text-sm py-1 px-3 rounded-full">{bookings.length}</span>
          </h2>
          {bookings.length === 0 ? <p className="text-slate-500">No active bookings.</p> : bookings.map((b: any) => (
            <div key={b.id} className="mb-3 p-4 bg-slate-50 rounded-lg border border-slate-100">
              <p className="font-bold text-slate-800">{b.booking_reference}</p>
              <p className="text-sm text-slate-500 mb-2">Property #{b.property_id}</p>
              <div className="flex gap-2">
                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded capitalize font-medium">{b.status}</span>
                {b.payment_status && <span className="text-xs bg-slate-200 text-slate-700 px-2 py-1 rounded font-medium">{b.payment_status}</span>}
              </div>
            </div>
          ))}
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-md border-t-4 border-amber-500">
          <h2 className="text-xl font-bold text-slate-800 mb-4 flex items-center justify-between">
            Support Requests
            <span className="bg-amber-100 text-amber-800 text-sm py-1 px-3 rounded-full">{support.length}</span>
          </h2>
          {support.length === 0 ? <p className="text-slate-500">No support requests.</p> : support.map((s: any) => (
            <div key={s.id} className="mb-3 p-4 bg-slate-50 rounded-lg border border-slate-100">
              <p className="font-bold text-slate-700 truncate" title={s.subject}>{s.subject}</p>
              <p className="text-sm text-slate-500 mb-2 truncate" title={s.description}>{s.description}</p>
              <div className="flex gap-2">
                <span className="text-xs bg-amber-100 text-amber-800 px-2 py-1 rounded capitalize font-medium">{s.status.replace(/_/g, ' ')}</span>
                <span className={`text-xs px-2 py-1 rounded capitalize font-medium ${
                  s.priority === 'high' || s.priority === 'urgent' ? 'bg-red-100 text-red-800' : 'bg-slate-200 text-slate-700'
                }`}>{s.priority}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
