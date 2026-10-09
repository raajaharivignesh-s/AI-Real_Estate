import { useEffect, useState } from 'react'

function App() {
  const [health, setHealth] = useState<string>('Loading...')

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/health')
      .then(res => res.json())
      .then(data => setHealth(data.status))
      .catch(err => setHealth('Error: ' + err.message))
  }, [])

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-xl shadow-md text-center max-w-md w-full">
        <h1 className="text-2xl font-bold text-slate-800 mb-4">AI Real Estate Assistant</h1>
        <p className="text-slate-600 mb-2">Frontend is running via Vite + React + Tailwind v4.</p>
        <div className="mt-4 p-4 rounded-lg bg-slate-100">
          <p className="text-sm font-medium text-slate-700">Backend Health Status:</p>
          <p className={`text-lg font-bold ${health === 'ok' ? 'text-green-600' : 'text-amber-600'}`}>
            {health}
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
