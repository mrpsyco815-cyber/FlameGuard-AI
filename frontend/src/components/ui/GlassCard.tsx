import type { HTMLAttributes, ReactNode } from 'react'

interface EditorialCardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode
  className?: string
  variant?: 'dark' | 'charcoal' | 'light'
}

export function EditorialCard({
  children,
  className = '',
  variant = 'dark',
  ...rest
}: EditorialCardProps) {
  const variantClass =
    variant === 'light'
      ? 'light-panel'
      : variant === 'charcoal'
      ? 'dark-panel-charcoal'
      : 'dark-panel'

  return (
    <div className={`${variantClass} ${className}`} {...rest}>
      {children}
    </div>
  )
}

// Backward compatibility alias for existing imports
export const GlassCard = EditorialCard
