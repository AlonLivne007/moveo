import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from './useAuth'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading, checked } = useAuth()
  const location = useLocation()

  if (!checked || loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        Loading...
      </div>
    )
  }
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }
  if (!user.onboarded) {
    return <Navigate to="/onboarding" replace />
  }
  return <>{children}</>
}

export function OnboardingRoute({ children }: { children: React.ReactNode }) {
  const { user, loading, checked } = useAuth()
  const location = useLocation()

  if (!checked || loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        Loading...
      </div>
    )
  }
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }
  if (user.onboarded) {
    return <Navigate to="/dashboard" replace />
  }
  return <>{children}</>
}
