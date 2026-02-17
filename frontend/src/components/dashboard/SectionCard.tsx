import type { CSSProperties, ReactNode } from 'react'

interface SectionCardProps {
  title: string
  children: ReactNode
}

export function SectionCard({ title, children }: SectionCardProps) {
  return (
    <section style={styles.card}>
      <h3 style={styles.title}>{title}</h3>
      {children}
    </section>
  )
}

const styles: Record<string, CSSProperties> = {
  card: { background: '#1e293b', borderRadius: 12, padding: 24, marginBottom: 24, border: '1px solid #334155' },
  title: { margin: '0 0 16px', color: '#f8fafc', fontSize: 18, fontWeight: 600 },
}
