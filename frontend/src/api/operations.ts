const API_URL = 'http://localhost:8000/api/v1';

export const getVisits = async () => {
  const token = localStorage.getItem('token');
  const res = await fetch(`${API_URL}/visits`, { headers: { 'Authorization': `Bearer ${token}` }});
  if (!res.ok) throw new Error('Failed to fetch visits');
  return res.json();
};

export const getBookings = async () => {
  const token = localStorage.getItem('token');
  const res = await fetch(`${API_URL}/bookings`, { headers: { 'Authorization': `Bearer ${token}` }});
  if (!res.ok) throw new Error('Failed to fetch bookings');
  return res.json();
};

export const getSupportRequests = async () => {
  const token = localStorage.getItem('token');
  const res = await fetch(`${API_URL}/support/requests`, { headers: { 'Authorization': `Bearer ${token}` }});
  if (!res.ok) throw new Error('Failed to fetch support requests');
  return res.json();
};
