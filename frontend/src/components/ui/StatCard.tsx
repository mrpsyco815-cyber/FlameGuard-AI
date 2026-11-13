import type { LucideIcon } from 'lucide-react'

interface StatCardProps {
  label: string
  value: string | number
  detail?: string
  icon?: LucideIcon
  highlight?: boolean
}

export function StatCard({
  label,
  value,
  detail,
  icon: Icon,
  highlight = false,
}: StatCardProps) {
  return (
    <div className="stat-card-dark">
      <div className="stat-card-top">
        <span className="stat-card-label">{label}</span>
        {Icon && (
          <div
            className="stat-card-icon"
            style={highlight ? { color: '#D96C32' } : undefined}
          >
            <Icon size={16} />
          </div>
        )}
      </div>
      <div>
        <div
          className="stat-card-value"
          style={highlight ? { color: '#D96C32' } : undefined}
        >
          {value}
        </div>
        {detail && <div className="stat-card-detail">{detail}</div>}
      </div>
    </div>
  )
}
