import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Heart } from 'lucide-react';
import { addToWishlist } from '../../api/wishlist';

export const PropertyCard = ({ property, onWishlistUpdate }: { property: any, onWishlistUpdate?: () => void }) => {
  const [isWishlisted, setIsWishlisted] = useState(false);

  const handleWishlist = async () => {
    try {
      await addToWishlist(property.id);
      setIsWishlisted(true);
      if (onWishlistUpdate) onWishlistUpdate();
    } catch (e) {
      console.error('Error adding to wishlist', e);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition">
      <div className="h-48 bg-slate-200 relative">
        {property.image_urls?.[0] && (
          <img src={property.image_urls[0]} alt={property.title} className="w-full h-full object-cover" />
        )}
        <button 
          onClick={handleWishlist} 
          className={`absolute top-2 right-2 p-2 bg-white rounded-full shadow-sm transition ${isWishlisted ? 'text-red-500' : 'text-slate-400 hover:text-red-500'}`}
        >
          <Heart size={20} fill={isWishlisted ? "currentColor" : "none"} />
        </button>
      </div>
      <div className="p-4">
        <h3 className="text-lg font-bold text-slate-800 mb-1 truncate">{property.title}</h3>
        <p className="text-sm text-slate-500 mb-3">{property.locality}, {property.city}</p>
        <div className="flex justify-between items-end">
          <p className="text-xl font-bold text-teal-600">₹{property.price.toLocaleString()}</p>
          <Link to={`/properties/${property.id}`} className="text-sm font-medium text-slate-700 hover:text-teal-600 transition">View Details &rarr;</Link>
        </div>
      </div>
    </div>
  );
};
