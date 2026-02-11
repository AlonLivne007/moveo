import type { AiInsightPayload, VoteResponse } from '../../types'
import { SectionCard } from './SectionCard'
import { VoteButtons } from './VoteButtons'

interface Props {
  insight: AiInsightPayload | null
  votes: VoteResponse[]
  onVote: (section_type: string, content_id: number, vote_value: number) => void
}

export function AiInsightSection({ insight, votes, onVote }: Props) {
  if (!insight) {
    return (
      <SectionCard title="AI Insight of the Day">
        <p style={styles.empty}>No insight available.</p>
      </SectionCard>
    )
  }
  return (
    <SectionCard title="AI Insight of the Day">
      <p style={styles.text}>{insight.text}</p>
      {insight.model_name && <span style={styles.model}>{insight.model_name}</span>}
      <VoteButtons sectionType="AI_INSIGHT" contentId={insight.id} votes={votes} onVote={onVote} />
    </SectionCard>
  )
}

const styles: Record<string, React.CSSProperties> = {
  text: { margin: '0 0 8px', color: '#e2e8f0', lineHeight: 1.6 },
  model: { fontSize: 12, color: '#64748b' },
  empty: { color: '#64748b', margin: 0 },
}
