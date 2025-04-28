import { useState } from 'react'
import './App.css'

function App() {
  const [resp, setResp] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const callPing = async () => {
    setLoading(true)
    setError(null)
    try {
      const baseUrl = import.meta.env.REACT_APP_BASE_URL || 'http://localhost:8000';
      console.log(`Calling ${baseUrl}/ping`)
      const res = await fetch(`${baseUrl}/ping`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setResp(data.message)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>PDFToolbox Frontend</h1>
      <button onClick={callPing} disabled={loading}>
        {loading ? 'Loading...' : 'Call /ping'}
      </button>

      {resp && (
        <div className="response">
          <strong>Response:</strong> {resp}
        </div>
      )}
      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}
    </div>
  )
}

export default App
