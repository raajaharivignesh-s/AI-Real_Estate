import { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { getProperty } from '../../api/properties';

export const ComparePage = () => {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const ids = params.getAll('id');
  
  const [properties, setProperties] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (ids.length === 0) {
      setLoading(false);
      return;
    }
    
    Promise.all(ids.map(id => getProperty(Number(id))))
      .then(data => {
        setProperties(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [ids.join(',')]);

  if (loading) return <div className="p-8 text-center text-slate-600">Loading comparison...</div>;

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8 overflow-x-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Compare Properties</h1>
        <Link to="/properties" className="text-teal-600 font-medium hover:underline">Back to Properties</Link>
      </div>
      
      {properties.length === 0 ? (
        <p className="text-slate-500 bg-white p-8 rounded-xl shadow-sm text-center">No properties selected for comparison.</p>
      ) : (
        <table className="w-full bg-white rounded-xl shadow-md text-left overflow-hidden">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="p-4 font-bold text-slate-700 w-1/4">Feature</th>
              {properties.map(p => (
                <th key={p.id} className="p-4 font-bold text-slate-800 min-w-[250px] align-top">
                  {p.image_urls?.[0] && <img src={p.image_urls[0]} alt={p.title} className="w-full h-32 object-cover rounded mb-3" />}
                  <div className="mb-2">{p.title}</div>
                  <Link to={`/properties/${p.id}`} className="text-sm font-normal text-teal-600 hover:underline">View details</Link>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-slate-100 hover:bg-slate-50 transition">
              <td className="p-4 font-medium text-slate-600">Price</td>
              {properties.map(p => <td key={p.id} className="p-4 text-teal-600 font-bold">₹{p.price.toLocaleString()}</td>)}
            </tr>
            <tr className="border-b border-slate-100 hover:bg-slate-50 transition">
              <td className="p-4 font-medium text-slate-600">Type</td>
              {properties.map(p => <td key={p.id} className="p-4 capitalize">{p.property_type}</td>)}
            </tr>
            <tr className="border-b border-slate-100 hover:bg-slate-50 transition">
              <td className="p-4 font-medium text-slate-600">Location</td>
              {properties.map(p => <td key={p.id} className="p-4">{p.locality}, {p.city}</td>)}
            </tr>
            <tr className="border-b border-slate-100 hover:bg-slate-50 transition">
              <td className="p-4 font-medium text-slate-600">Area</td>
              {properties.map(p => <td key={p.id} className="p-4">{p.area_sqft} sqft</td>)}
            </tr>
            <tr className="border-b border-slate-100 hover:bg-slate-50 transition">
              <td className="p-4 font-medium text-slate-600">Bedrooms</td>
              {properties.map(p => <td key={p.id} className="p-4">{p.bedrooms || 'N/A'}</td>)}
            </tr>
            <tr className="border-b border-slate-100 hover:bg-slate-50 transition">
              <td className="p-4 font-medium text-slate-600">Bathrooms</td>
              {properties.map(p => <td key={p.id} className="p-4">{p.bathrooms || 'N/A'}</td>)}
            </tr>
            <tr className="hover:bg-slate-50 transition">
              <td className="p-4 font-medium text-slate-600">Amenities</td>
              {properties.map(p => <td key={p.id} className="p-4 text-sm text-slate-600 leading-relaxed">{p.amenities?.join(', ') || 'None'}</td>)}
            </tr>
          </tbody>
        </table>
      )}
    </div>
  );
};
