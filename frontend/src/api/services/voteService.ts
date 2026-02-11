import { api } from '../axios'
import type { VoteResponse } from '../../types'

export const voteService = {
  async vote(section_type: string, content_id: number, vote_value: number): Promise<VoteResponse> {
    const { data } = await api.post<VoteResponse>('/api/votes', { section_type, content_id, vote_value })
    return data
  },
  async getTodayVotes(): Promise<VoteResponse[]> {
    const { data } = await api.get<{ votes: VoteResponse[] }>('/api/votes/today')
    return data.votes
  },
}
