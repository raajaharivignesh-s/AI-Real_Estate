const API_URL = 'http://localhost:8000/api/v1';

export const getProperties = async (filters: any = {}) => {
  const query = new URLSearchParams(filters).toString();
  const res = await fetch(`${API_URL}/properties?${query}`);
  if (!res.ok) throw new Error('Failed to fetch properties');
  return res.json();
};

export const getProperty = async (id: number) => {
  const res = await fetch(`${API_URL}/properties/${id}`);
  if (!res.ok) throw new Error('Failed to fetch property');
  return res.json();
};
