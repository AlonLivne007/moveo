import type { CSSProperties } from 'react'
import type { VoteResponse } from '../../types'

type SectionType = 'NEWS' | 'PRICES' | 'AI_INSIGHT' | 'MEME'

interface VoteButtonsProps {
  sectionType: SectionType
  contentId: number
  votes: VoteResponse[]
  onVote: (section_type: string, content_id: number, vote_value: number) => void
  voted?: boolean
}

export function VoteButtons({ sectionType, contentId, votes, onVote, voted }: VoteButtonsProps) {
  const current = votes.find((v) => v.section_type === sectionType && v.content_id === contentId)
  const value = current?.vote_value ?? 0

  return (
    <div style={styles.wrapper}>
      <button
        type="button"
        onClick={() => onVote(sectionType, contentId, 1)}
        style={{ ...styles.btn, ...(value === 1 ? styles.btnActive : {}) }}
        title="Thumbs up"
      >
        👍
      </button>
      <button
        type="button"
        onClick={() => onVote(sectionType, contentId, -1)}
        style={{ ...styles.btn, ...(value === -1 ? styles.btnActive : {}) }}
        title="Thumbs down"
      >
        👎
      </button>
      {(voted ?? value !== 0) && <span style={styles.thanks}>Thanks for feedback!</span>}
    </div>
  )
}

const styles: Record<string, CSSProperties> = {
  wrapper: { display: 'flex', alignItems: 'center', gap: 8, marginTop: 12 },
  btn: { padding: '6px 12px', borderRadius: 8, border: '1px solid #475569', background: '#0f172a', cursor: 'pointer', fontSize: 16 },
  btnActive: { background: '#334155', borderColor: '#64748b' },
  thanks: { color: '#86efac', fontSize: 13, marginLeft: 8 },
}
