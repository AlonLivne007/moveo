import { api } from '../axios'
import type { UserProfile } from '../../types'

export const authService = {
  async signup(name: string, email: string, password: string) {
    const { data } = await api.post<{ access_token: string }>('/api/auth/signup', { name, email, password })
    return data
  },
  async login(email: string, password: string) {
    const { data } = await api.post<{ access_token: string }>('/api/auth/login', { email, password })
    return data
  },
  async me(): Promise<UserProfile> {
    const { data } = await api.get<UserProfile>('/api/me')
    return data
  },
}
