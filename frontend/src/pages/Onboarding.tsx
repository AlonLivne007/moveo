import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { onboardingService } from '../api/services/onboardingService'

const ASSET_OPTIONS = ['Bitcoin', 'Ethereum', 'Solana', 'Cardano', 'Polkadot', 'Avalanche', 'Chainlink', 'Polygon', 'Dogecoin', 'Other']
const INVESTOR_TYPES = ['HODLer', 'Day Trader', 'NFT Collector', 'Other']
const CONTENT_TYPES = ['Market News', 'Charts', 'Social', 'Fun']

export function Onboarding() {
  const [assets, setAssets] = useState<string[]>([])
  const [investorType, setInvestorType] = useState('')
  const [contentTypes, setContentTypes] = useState<string[]>([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [voted, setVoted] = useState(false)
  const navigate = useNavigate()

  function toggleAsset(a: string) {
    setAssets((prev) => (prev.includes(a) ? prev.filter((x) => x !== a) : [...prev, a]))
  }
  function toggleContent(c: string) {
    setContentTypes((prev) => (prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]))
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!investorType) {
      setError('Please select an investor type')
      return
    }
    setError('')
    setLoading(true)
    try {
      const assetIds = assets.map((a) => a.toLowerCase().replace(' ', '-'))
      if (assetIds.includes('other')) {
        const i = assetIds.indexOf('other')
        assetIds[i] = 'bitcoin'
      }
      await onboardingService.submit(assetIds, investorType, contentTypes.length ? contentTypes : ['Market News', 'Fun'])
      setVoted(true)
      setTimeout(() => navigate('/dashboard', { replace: true }), 800)
    } catch {
      setError('Failed to save preferences')
    } finally {
      setLoading(false)
    }
  }

  if (voted) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <p style={styles.thanks}>Thanks for your feedback! Redirecting to dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Welcome! Set your preferences</h1>
        <form onSubmit={handleSubmit} style={styles.form}>
          {error && <p style={styles.error}>{error}</p>}
          <label style={styles.label}>What crypto assets are you interested in?</label>
          <div style={styles.chips}>
            {ASSET_OPTIONS.map((a) => (
              <button
                key={a}
                type="button"
                onClick={() => toggleAsset(a)}
                style={{ ...styles.chip, ...(assets.includes(a) ? styles.chipActive : {}) }}
              >
                {a}
              </button>
            ))}
          </div>
          <label style={styles.label}>What type of investor are you?</label>
          <select
            value={investorType}
            onChange={(e) => setInvestorType(e.target.value)}
            style={styles.select}
            required
          >
            <option value="">Select...</option>
            {INVESTOR_TYPES.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
          <label style={styles.label}>What content do you want to see?</label>
          <div style={styles.chips}>
            {CONTENT_TYPES.map((c) => (
              <button
                key={c}
                type="button"
                onClick={() => toggleContent(c)}
                style={{ ...styles.chip, ...(contentTypes.includes(c) ? styles.chipActive : {}) }}
              >
                {c}
              </button>
            ))}
          </div>
          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? 'Saving...' : 'Save & go to dashboard'}
          </button>
        </form>
      </div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', background: '#0f172a', padding: 24 },
  card: { maxWidth: 560, margin: '0 auto', background: '#1e293b', borderRadius: 12, padding: 32, boxShadow: '0 4px 20px rgba(0,0,0,0.3)' },
  title: { margin: '0 0 24px', color: '#f8fafc', fontSize: 22 },
  form: { display: 'flex', flexDirection: 'column', gap: 20 },
  error: { color: '#f87171', margin: 0, fontSize: 14 },
  label: { color: '#94a3b8', fontSize: 14, fontWeight: 500 },
  chips: { display: 'flex', flexWrap: 'wrap', gap: 8 },
  chip: { padding: '8px 14px', borderRadius: 20, border: '1px solid #334155', background: '#0f172a', color: '#94a3b8', cursor: 'pointer', fontSize: 14 },
  chipActive: { background: '#3b82f6', color: 'white', borderColor: '#3b82f6' },
  select: { padding: '12px 16px', borderRadius: 8, border: '1px solid #334155', background: '#0f172a', color: '#f8fafc', fontSize: 16 },
  button: { padding: 12, borderRadius: 8, border: 'none', background: '#3b82f6', color: 'white', fontSize: 16, cursor: 'pointer', fontWeight: 600, marginTop: 8 },
  thanks: { color: '#86efac', margin: 0, fontSize: 16 },
}
