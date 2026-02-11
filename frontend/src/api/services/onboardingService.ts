import { api } from '../axios'

export const onboardingService = {
  async submit(assets: string[], investor_type: string, content_types: string[]) {
    await api.post('/api/onboarding', { assets, investor_type, content_types })
  },
  async getPreferences() {
    const { data } = await api.get<{ assets: string[]; investor_type: string; content_types: string[] }>('/api/onboarding/preferences')
    return data
  },
}
