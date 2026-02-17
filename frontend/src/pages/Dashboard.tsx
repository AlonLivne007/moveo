import { useEffect, useState, type CSSProperties } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/useAuth'
import { dashboardService } from '../api/services/dashboardService'
import { voteService } from '../api/services/voteService'
import type { DashboardResponse, VoteResponse } from '../types'
import { MarketNewsSection } from '../components/dashboard/MarketNewsSection'
import { PricesSection } from '../components/dashboard/PricesSection'
import { AiInsightSection } from '../components/dashboard/AiInsightSection'
import { MemeSection } from '../components/dashboard/MemeSection'

export function Dashboard() {
  const { user, logout } = useAuth()
  const [data, setData] = useState<DashboardResponse | null>(null)
  const [votes, setVotes] = useState<VoteResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const [d, v] = await Promise.all([dashboardService.getToday(), voteService.getTodayVotes()])
        if (!cancelled) {
          setData(d)
          setVotes(v)
        }
      } catch {
        if (!cancelled) setError('Failed to load dashboard')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  async function handleVote(section_type: string, content_id: number, vote_value: number) {
    try {
      await voteService.vote(section_type, content_id, vote_value)
      setVotes((prev) => {
        const rest = prev.filter((x) => !(x.section_type === section_type && x.content_id === content_id))
        return [...rest, { id: 0, section_type, content_id, vote_value, created_at: '' }]
      })
    } catch {
      // ignore
    }
  }

  if (loading) {
    return (
      <div style={styles.wrapper}>
        <header style={styles.header}>
          <span style={styles.logo}>AI Crypto Advisor</span>
          <span style={styles.user}>{user?.name}</span>
          <button type="button" onClick={() => { logout(); navigate('/login'); }} style={styles.logoutBtn}>Log out</button>
        </header>
        <div style={styles.loading}>Loading dashboard...</div>
      </div>
    )
  }
  if (error || !data) {
    return (
      <div style={styles.wrapper}>
        <header style={styles.header}>
          <span style={styles.logo}>AI Crypto Advisor</span>
          <button type="button" onClick={() => navigate('/login')} style={styles.logoutBtn}>Log out</button>
        </header>
        <div style={styles.loading}>{error || 'No data'}</div>
      </div>
    )
  }

  return (
    <div style={styles.wrapper}>
      <header style={styles.header}>
        <span style={styles.logo}>AI Crypto Advisor</span>
        <span style={styles.user}>{user?.name}</span>
        <button type="button" onClick={() => { logout(); navigate('/login'); }} style={styles.logoutBtn}>Log out</button>
      </header>
      <main style={styles.main}>
        <h2 style={styles.date}>Dashboard — {data.date}</h2>
        <MarketNewsSection items={data.news} votes={votes} onVote={handleVote} />
        <PricesSection prices={data.prices} votes={votes} onVote={handleVote} />
        <AiInsightSection insight={data.ai_insight} votes={votes} onVote={handleVote} />
        <MemeSection meme={data.meme} votes={votes} onVote={handleVote} />
      </main>
    </div>
  )
}

const styles: Record<string, CSSProperties> = {
  wrapper: { minHeight: '100vh', background: '#0f172a', color: '#f8fafc' },
  header: { display: 'flex', alignItems: 'center', gap: 16, padding: '16px 24px', borderBottom: '1px solid #334155', background: '#1e293b' },
  logo: { fontSize: 20, fontWeight: 700 },
  user: { color: '#94a3b8', marginLeft: 'auto' },
  logoutBtn: { padding: '8px 16px', borderRadius: 8, border: '1px solid #475569', background: 'transparent', color: '#94a3b8', cursor: 'pointer', fontSize: 14 },
  main: { padding: 24, maxWidth: 900, margin: '0 auto' },
  date: { margin: '0 0 24px', color: '#94a3b8', fontSize: 16, fontWeight: 400 },
  loading: { padding: 48, textAlign: 'center', color: '#94a3b8' },
}
