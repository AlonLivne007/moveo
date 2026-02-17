import type { CSSProperties } from 'react'
import type { PricesPayload, VoteResponse } from '../../types'
import { SectionCard } from './SectionCard'
import { VoteButtons } from './VoteButtons'

interface Props {
  prices: PricesPayload | null
  votes: VoteResponse[]
  onVote: (section_type: string, content_id: number, vote_value: number) => void
}

export function PricesSection({ prices, votes, onVote }: Props) {
  if (!prices || !prices.items?.length) {
    return (
      <SectionCard title="Coin Prices">
        <p style={styles.empty}>No price data available.</p>
      </SectionCard>
    )
  }
  return (
    <SectionCard title="Coin Prices">
      <ul style={styles.list}>
        {prices.items.map((p) => (
          <li key={p.id} style={styles.row}>
            <span style={styles.symbol}>{p.symbol}</span>
            <span style={styles.name}>{p.name}</span>
            <span style={styles.price}>${p.current_price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })}</span>
            {p.change_24h != null && (
              <span style={p.change_24h >= 0 ? styles.changeUp : styles.changeDown}>
                {(p.change_24h >= 0 ? '+' : '') + p.change_24h.toFixed(2)}% 24h
              </span>
            )}
          </li>
        ))}
      </ul>
      <VoteButtons sectionType="PRICES" contentId={prices.snapshot_id} votes={votes} onVote={onVote} />
    </SectionCard>
  )
}

const styles: Record<string, CSSProperties> = {
  list: { listStyle: 'none', margin: 0, padding: 0 },
  row: { display: 'flex', alignItems: 'center', gap: 12, padding: '8px 0', borderBottom: '1px solid #334155', flexWrap: 'wrap' },
  symbol: { fontWeight: 600, minWidth: 60 },
  name: { color: '#94a3b8', flex: 1 },
  price: { color: '#f8fafc' },
  changeUp: { fontSize: 14, color: '#86efac' },
  changeDown: { fontSize: 14, color: '#f87171' },
  empty: { color: '#64748b', margin: 0 },
}
