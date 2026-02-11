import type { NewsItemPayload, VoteResponse } from '../../types'
import { SectionCard } from './SectionCard'
import { VoteButtons } from './VoteButtons'

interface Props {
  items: NewsItemPayload[]
  votes: VoteResponse[]
  onVote: (section_type: string, content_id: number, vote_value: number) => void
}

export function MarketNewsSection({ items, votes, onVote }: Props) {
  return (
    <SectionCard title="Market News">
      <ul style={styles.list}>
        {items.map((item) => (
          <li key={item.id} style={styles.item}>
            <a href={item.link || '#'} target="_blank" rel="noopener noreferrer" style={styles.link}>
              {item.title}
            </a>
            {(item.source || item.published_at) && (
              <span style={styles.meta}>
                {item.source}
                {item.published_at && ' · ' + new Date(item.published_at).toLocaleDateString()}
              </span>
            )}
            <VoteButtons sectionType="NEWS" contentId={item.id} votes={votes} onVote={onVote} />
          </li>
        ))}
      </ul>
    </SectionCard>
  )
}

const styles: Record<string, React.CSSProperties> = {
  list: { listStyle: 'none', margin: 0, padding: 0 },
  item: { paddingBottom: 16, marginBottom: 16, borderBottom: '1px solid #334155' },
  link: { color: '#60a5fa', textDecoration: 'none', fontSize: 15 },
  meta: { display: 'block', color: '#64748b', fontSize: 13, marginTop: 4 },
}
