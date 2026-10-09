const API_URL = 'http://localhost:8000/api/v1';

export const getWishlist = async () => {
  const token = localStorage.getItem('token');
  const res = await fetch(`${API_URL}/wishlist`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to fetch wishlist');
  return res.json();
};

export const addToWishlist = async (id: number) => {
  const token = localStorage.getItem('token');
  const res = await fetch(`${API_URL}/wishlist/${id}`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to add to wishlist');
  return res.json();
};

export const removeFromWishlist = async (id: number) => {
  const token = localStorage.getItem('token');
  const res = await fetch(`${API_URL}/wishlist/${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) throw new Error('Failed to remove from wishlist');
  return res.json();
};
