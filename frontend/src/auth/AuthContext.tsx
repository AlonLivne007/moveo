import { createContext, useCallback, useEffect, useState, type ReactNode } from 'react'
import { authService } from '../api/services/authService'
import type { UserProfile } from '../types'

interface AuthState {
  user: UserProfile | null
  loading: boolean
  checked: boolean
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>
  signup: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
  refreshProfile: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({ user: null, loading: true, checked: false })

  const refreshProfile = useCallback(async () => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setState({ user: null, loading: false, checked: true })
      return
    }
    try {
      const user = await authService.me()
      setState({ user, loading: false, checked: true })
    } catch {
      localStorage.removeItem('access_token')
      setState({ user: null, loading: false, checked: true })
    }
  }, [])

  useEffect(() => {
    refreshProfile()
  }, [refreshProfile])

  useEffect(() => {
    const onLogout = () => setState({ user: null, loading: false, checked: true })
    window.addEventListener('auth:logout', onLogout)
    return () => window.removeEventListener('auth:logout', onLogout)
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    setState((s) => ({ ...s, loading: true }))
    const { access_token } = await authService.login(email, password)
    localStorage.setItem('access_token', access_token)
    await refreshProfile()
  }, [refreshProfile])

  const signup = useCallback(async (name: string, email: string, password: string) => {
    setState((s) => ({ ...s, loading: true }))
    const { access_token } = await authService.signup(name, email, password)
    localStorage.setItem('access_token', access_token)
    await refreshProfile()
  }, [refreshProfile])

  const logout = useCallback(() => {
    localStorage.removeItem('access_token')
    setState({ user: null, loading: false, checked: true })
  }, [])

  const value: AuthContextValue = {
    ...state,
    login,
    signup,
    logout,
    refreshProfile,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
