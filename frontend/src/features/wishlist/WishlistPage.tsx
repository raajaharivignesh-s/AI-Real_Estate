import { useState, useEffect } from 'react';
import { getWishlist, removeFromWishlist } from '../../api/wishlist';
import { Link } from 'react-router-dom';
import { Trash2 } from 'lucide-react';

export const WishlistPage = () => {
  const [properties, setProperties] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchWishlist = () => {
    getWishlist().then(data => {
      setProperties(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => {
    fetchWishlist();
  }, []);

  const handleRemove = async (id: number) => {
    await removeFromWishlist(id);
    fetchWishlist();
  };

  if (loading) return <div className="p-8 text-center text-slate-600">Loading wishlist...</div>;

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">My Wishlist</h1>
        <Link to="/properties" className="text-teal-600 font-medium hover:underline">Back to Properties</Link>
      </div>
      {properties.length === 0 ? (
        <p className="text-slate-500 bg-white p-8 rounded-xl shadow-sm text-center">Your wishlist is empty.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {properties.map(p => (
            <div key={p.id} className="bg-white rounded-xl shadow-md overflow-hidden relative hover:shadow-lg transition">
               <button onClick={() => handleRemove(p.id)} className="absolute top-2 right-2 p-2 bg-white rounded-full text-red-500 hover:bg-red-50 z-10 shadow transition">
                  <Trash2 size={20} />
               </button>
               <div className="h-48 bg-slate-200">
                  {p.image_urls?.[0] && <img src={p.image_urls[0]} alt={p.title} className="w-full h-full object-cover" />}
               </div>
               <div className="p-4">
                  <h3 className="text-lg font-bold text-slate-800 truncate mb-1">{p.title}</h3>
                  <p className="text-teal-600 font-bold mb-3">₹{p.price.toLocaleString()}</p>
                  <Link to={`/properties/${p.id}`} className="text-sm font-medium text-slate-700 hover:text-teal-600 transition">View Details &rarr;</Link>
               </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
