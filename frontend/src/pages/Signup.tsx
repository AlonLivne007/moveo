import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'

const formStyles = {
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

export function Signup() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { signup } = useAuth()
  const navigate = useNavigate()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await signup(name, email, password)
      navigate('/onboarding', { replace: true })
    } catch (err: unknown) {
      const res = err && typeof err === 'object' && 'response' in err ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail : null
      setError(typeof res === 'string' ? res : 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={formStyles.container}>
      <div style={formStyles.card}>
        <h1 style={formStyles.title}>AI Crypto Advisor</h1>
        <h2 style={formStyles.subtitle}>Create account</h2>
        <form onSubmit={handleSubmit} style={formStyles.form}>
          {error && <p style={formStyles.error}>{error}</p>}
          <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required style={formStyles.input} />
          <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required style={formStyles.input} />
          <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required style={formStyles.input} />
          <button type="submit" disabled={loading} style={formStyles.button}>
            {loading ? 'Creating account...' : 'Sign up'}
          </button>
        </form>
        <p style={formStyles.footer}>
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </div>
    </div>
  )
}
