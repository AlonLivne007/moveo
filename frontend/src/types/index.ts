export interface UserProfile {
  id: number
  name: string
  email: string
  onboarded: boolean
}

export interface NewsItemPayload {
  id: number
  title: string
  source: string | null
  published_at: string | null
  link: string | null
  /** Optional; API may send link or url depending on backend */
  url?: string | null
}

export interface PriceItemPayload {
  id: string
  symbol: string
  name: string
  current_price: number
  change_24h: number | null
}

export interface PricesPayload {
  snapshot_id: number
  items: PriceItemPayload[]
}

export interface AiInsightPayload {
  id: number
  text: string
  model_name: string | null
}

export interface MemePayload {
  id: number
  title: string | null
  image_url: string
  post_url: string | null
}

export interface DashboardResponse {
  date: string
  news: NewsItemPayload[]
  prices: PricesPayload | null
  ai_insight: AiInsightPayload | null
  meme: MemePayload | null
}

export interface VoteResponse {
  id: number
  section_type: string
  content_id: number
  vote_value: number
  created_at: string
}

export type SectionType = 'NEWS' | 'PRICES' | 'AI_INSIGHT' | 'MEME'
