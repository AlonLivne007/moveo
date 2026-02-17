import type { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from './useAuth'

const loadingStyle = { padding: '2rem', textAlign: 'center' as const }

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user, loading, checked } = useAuth()
  const location = useLocation()

  if (!checked || loading) return <div style={loadingStyle}>Loading...</div>
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />
  if (!user.onboarded) return <Navigate to="/onboarding" replace />
  return <>{children}</>
}

export function OnboardingRoute({ children }: { children: ReactNode }) {
  const { user, loading, checked } = useAuth()
  const location = useLocation()

  if (!checked || loading) return <div style={loadingStyle}>Loading...</div>
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />
  if (user.onboarded) return <Navigate to="/dashboard" replace />
  return <>{children}</>
}
