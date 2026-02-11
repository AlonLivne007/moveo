import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'

export function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: { pathname: string } })?.from?.pathname || '/dashboard'

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate(from, { replace: true })
    } catch (err: unknown) {
      setError(err && typeof err === 'object' && 'response' in err && typeof (err as { response?: { data?: { detail?: string } } }).response?.data?.detail === 'string'
        ? (err as { response: { data: { detail: string } } }).response.data.detail
        : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>AI Crypto Advisor</h1>
        <h2 style={styles.subtitle}>Log in</h2>
        <form onSubmit={handleSubmit} style={styles.form}>
          {error && <p style={styles.error}>{error}</p>}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={styles.input}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={styles.input}
          />
          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'Logging in...' : 'Log in'}
          </button>
        </form>
        <p style={styles.footer}>
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#0f172a', padding: 16 },
  card: { background: '#1e293b', borderRadius: 12, padding: 32, width: '100%', maxWidth: 400, boxShadow: '0 4px 20px rgba(0,0,0,0.3)' },
  title: { margin: '0 0 8px', color: '#f8fafc', fontSize: 24 },
  subtitle: { margin: '0 0 24px', color: '#94a3b8', fontSize: 18, fontWeight: 400 },
  form: { display: 'flex', flexDirection: 'column', gap: 16 },
  error: { color: '#f87171', margin: 0, fontSize: 14 },
  input: { padding: '12px 16px', borderRadius: 8, border: '1px solid #334155', background: '#0f172a', color: '#f8fafc', fontSize: 16 },
  button: { padding: 12, borderRadius: 8, border: 'none', background: '#3b82f6', color: 'white', fontSize: 16, cursor: 'pointer', fontWeight: 600 },
  footer: { marginTop: 24, color: '#94a3b8', fontSize: 14 },
}
