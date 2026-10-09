import { useState } from 'react';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';

export const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await login({ email, password });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold text-slate-800 mb-6 text-center">Sign In</h2>
        {error && <div className="bg-red-50 text-red-600 p-3 rounded-md mb-4 text-sm">{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
            <input 
              type="email" 
              value={email}
              onChange={e => setEmail(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500" 
              required 
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={e => setPassword(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded-md focus:ring-2 focus:ring-teal-500 focus:border-teal-500" 
              required 
            />
          </div>
          <button type="submit" className="w-full bg-slate-800 text-white p-2 rounded-md hover:bg-slate-700 transition">
            Sign In
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-slate-600">
          Don't have an account? <a href="/register" className="text-teal-600 hover:underline">Register</a>
        </p>

        <div className="mt-8 bg-slate-100 p-4 rounded-lg border border-slate-200">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 text-center">Demo Accounts</h3>
          <div className="space-y-2 text-sm text-slate-700">
            <button 
              type="button"
              onClick={() => { setEmail('admin@demo.com'); setPassword('password123'); }}
              className="w-full text-left p-2 bg-white rounded border border-slate-200 hover:border-teal-500 transition group flex justify-between items-center"
            >
              <div>
                <div className="font-semibold group-hover:text-teal-700">Admin</div>
                <div className="text-xs text-slate-500">admin@demo.com / password123</div>
              </div>
              <span className="text-xs font-medium text-teal-600 opacity-0 group-hover:opacity-100 transition">Use</span>
            </button>
            <button 
              type="button"
              onClick={() => { setEmail('customer1@demo.com'); setPassword('password123'); }}
              className="w-full text-left p-2 bg-white rounded border border-slate-200 hover:border-teal-500 transition group flex justify-between items-center"
            >
              <div>
                <div className="font-semibold group-hover:text-teal-700">Customer</div>
                <div className="text-xs text-slate-500">customer1@demo.com / password123</div>
              </div>
              <span className="text-xs font-medium text-teal-600 opacity-0 group-hover:opacity-100 transition">Use</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
