import type { MemePayload, VoteResponse } from '../../types'
import { SectionCard } from './SectionCard'
import { VoteButtons } from './VoteButtons'

interface Props {
  meme: MemePayload | null
  votes: VoteResponse[]
  onVote: (section_type: string, content_id: number, vote_value: number) => void
}

export function MemeSection({ meme, votes, onVote }: Props) {
  if (!meme) {
    return (
      <SectionCard title="Fun Crypto Meme">
        <p style={styles.empty}>No meme today.</p>
      </SectionCard>
    )
  }
  return (
    <SectionCard title="Fun Crypto Meme">
      {meme.title && <p style={styles.title}>{meme.title}</p>}
      <a href={meme.post_url || '#'} target="_blank" rel="noopener noreferrer" style={styles.imgWrap}>
        <img src={meme.image_url} alt={meme.title || 'Crypto meme'} style={styles.img} />
      </a>
      <VoteButtons sectionType="MEME" contentId={meme.id} votes={votes} onVote={onVote} />
    </SectionCard>
  )
}

const styles: Record<string, React.CSSProperties> = {
  title: { margin: '0 0 12px', color: '#e2e8f0', fontSize: 15 },
  imgWrap: { display: 'block', marginBottom: 8 },
  img: { maxWidth: '100%', borderRadius: 8, border: '1px solid #334155' },
  empty: { color: '#64748b', margin: 0 },
}
