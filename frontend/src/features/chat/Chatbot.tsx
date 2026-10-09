import { useState } from 'react';
import { MessageSquare, X, Send } from 'lucide-react';
import { useAuth } from '../auth/AuthContext';

export const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{role: string, content: string}[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  if (!user) return null; // Only show for logged in users

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const newMsg = { role: 'user', content: input };
    const chatHistory = [...messages, newMsg];
    setMessages(chatHistory);
    setInput('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8000/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ messages: chatHistory })
      });
      if (!res.ok) throw new Error('API Error');
      const data = await res.json();
      setMessages([...chatHistory, { role: 'assistant', content: data.reply }]);
    } catch (err) {
      setMessages([...chatHistory, { role: 'assistant', content: 'Oops, something went wrong!' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isOpen ? (
        <button 
          onClick={() => setIsOpen(true)}
          className="bg-slate-800 hover:bg-slate-700 text-white p-4 rounded-full shadow-xl transition transform hover:scale-105"
        >
          <MessageSquare size={24} />
        </button>
      ) : (
        <div className="bg-white rounded-2xl shadow-2xl w-80 sm:w-96 overflow-hidden border border-slate-200 flex flex-col h-[500px]">
          <div className="bg-slate-800 text-white p-4 flex justify-between items-center">
            <h3 className="font-bold flex items-center gap-2">
              <MessageSquare size={18} /> Real Estate Assistant
            </h3>
            <button onClick={() => setIsOpen(false)} className="text-slate-300 hover:text-white transition">
              <X size={20} />
            </button>
          </div>
          
          <div className="flex-1 p-4 overflow-y-auto bg-slate-50 flex flex-col gap-3">
            {messages.length === 0 && (
              <p className="text-slate-500 text-center text-sm mt-4">
                Hi {user.full_name}! I can help you find properties, calculate EMIs, book site visits, or create support tickets. How can I help today?
              </p>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`max-w-[80%] rounded-xl p-3 text-sm ${m.role === 'user' ? 'bg-teal-600 text-white self-end rounded-br-none' : 'bg-white border border-slate-200 text-slate-700 self-start rounded-bl-none shadow-sm'}`}>
                {m.content}
              </div>
            ))}
            {loading && <div className="text-slate-400 text-xs self-start bg-white p-2 rounded border border-slate-200">Typing...</div>}
          </div>
          
          <form onSubmit={handleSend} className="p-3 bg-white border-t border-slate-200 flex gap-2">
            <input 
              type="text" 
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Type your message..." 
              className="flex-1 bg-slate-100 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
            <button type="submit" disabled={loading} className="bg-teal-600 text-white p-2 rounded-full hover:bg-teal-700 transition disabled:opacity-50">
              <Send size={18} />
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
