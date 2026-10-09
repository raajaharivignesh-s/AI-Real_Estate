import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProperty } from '../../api/properties';
import { addToWishlist } from '../../api/wishlist';

export const PropertyDetailsPage = () => {
  const { id } = useParams();
  const [property, setProperty] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProperty(Number(id)).then(data => {
      setProperty(data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="p-8 text-center text-slate-600">Loading details...</div>;
  if (!property) return <div className="p-8 text-center text-red-600">Property not found.</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 md:p-8">
      <Link to="/properties" className="text-teal-600 hover:underline mb-6 inline-block">&larr; Back to Listings</Link>
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="h-64 md:h-96 bg-slate-200">
          {property.image_urls?.[0] && <img src={property.image_urls[0]} alt={property.title} className="w-full h-full object-cover" />}
        </div>
        <div className="p-6 md:p-8">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-3xl font-bold text-slate-800 mb-2">{property.title}</h1>
              <p className="text-lg text-slate-500">{property.address}, {property.locality}, {property.city}</p>
            </div>
            <p className="text-3xl font-bold text-teal-600">₹{property.price.toLocaleString()}</p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 py-6 border-y border-slate-100">
            <div>
              <p className="text-sm text-slate-400">Type</p>
              <p className="font-semibold text-slate-700 capitalize">{property.property_type}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Area</p>
              <p className="font-semibold text-slate-700">{property.area_sqft} sqft</p>
            </div>
            {property.bedrooms && (
              <div>
                <p className="text-sm text-slate-400">Bedrooms</p>
                <p className="font-semibold text-slate-700">{property.bedrooms}</p>
              </div>
            )}
            {property.bathrooms && (
              <div>
                <p className="text-sm text-slate-400">Bathrooms</p>
                <p className="font-semibold text-slate-700">{property.bathrooms}</p>
              </div>
            )}
          </div>
          
          <div className="mb-8">
            <h2 className="text-xl font-bold text-slate-800 mb-3">Description</h2>
            <p className="text-slate-600 whitespace-pre-line">{property.description}</p>
          </div>
          
          {property.amenities?.length > 0 && (
            <div className="mb-8">
              <h2 className="text-xl font-bold text-slate-800 mb-3">Amenities</h2>
              <div className="flex flex-wrap gap-2">
                {property.amenities.map((a: string, idx: number) => (
                  <span key={idx} className="bg-teal-50 text-teal-700 px-3 py-1 rounded-full text-sm font-medium">{a}</span>
                ))}
              </div>
            </div>
          )}
          
          <div className="flex gap-4">
            <button onClick={() => addToWishlist(property.id).then(() => alert('Saved!')).catch(() => alert('Login required'))} className="bg-slate-800 text-white px-6 py-3 rounded-lg font-medium hover:bg-slate-700 transition flex-1">
              Save to Wishlist
            </button>
            <button className="bg-teal-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-teal-700 transition flex-1">
              Request Site Visit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
