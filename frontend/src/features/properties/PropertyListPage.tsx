import { useState, useEffect } from 'react';
import { getProperties } from '../../api/properties';
import { PropertyCard } from './PropertyCard';

export const PropertyListPage = () => {
  const [properties, setProperties] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProperties().then(data => {
      setProperties(data.items);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-8 text-center text-slate-600">Loading properties...</div>;

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Properties</h1>
        <a href="/wishlist" className="text-teal-600 font-medium hover:underline transition">My Wishlist</a>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {properties.map(p => <PropertyCard key={p.id} property={p} />)}
      </div>
    </div>
  );
};
