import type { ReactNode } from 'react'

interface SectionHeaderProps {
  eyebrow?: string
  title: string
  detail?: string
  action?: ReactNode
  dark?: boolean
}

export function SectionHeader({
  eyebrow,
  title,
  detail,
  action,
  dark = false,
}: SectionHeaderProps) {
  return (
    <div className="section-header">
      <div>
        {eyebrow && (
          <div className={`eyebrow ${dark ? 'eyebrow-dark' : ''}`}>
            {eyebrow}
          </div>
        )}
        <h2 className={`section-title ${dark ? 'section-title-dark' : ''}`}>
          {title}
        </h2>
        {detail && (
          <p className={`section-subtitle ${dark ? 'section-subtitle-dark' : ''}`}>
            {detail}
          </p>
        )}
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}
