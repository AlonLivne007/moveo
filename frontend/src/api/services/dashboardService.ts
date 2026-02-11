import { api } from '../axios'
import type { DashboardResponse } from '../../types'

export const dashboardService = {
  async getToday(): Promise<DashboardResponse> {
    const { data } = await api.get<DashboardResponse>('/api/dashboard/today')
    return data
  },
}
