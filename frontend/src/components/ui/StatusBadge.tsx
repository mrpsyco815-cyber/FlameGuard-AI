import type { ReactNode } from 'react'
import {
  CheckCircle2,
  CircleAlert,
  FileText,
  FlaskConical,
  HelpCircle,
  ShieldCheck,
  XCircle,
} from 'lucide-react'

export interface StatusBadgeProps {
  children: ReactNode
  tone?: 'verified' | 'warning' | 'unverified' | 'neutral' | 'orange'
}

export function StatusBadge({ children, tone = 'neutral' }: StatusBadgeProps) {
  const toneClass =
    tone === 'verified'
      ? 'badge-verified'
      : tone === 'warning'
      ? 'badge-warning'
      : tone === 'unverified'
      ? 'badge-unverified'
      : tone === 'orange'
      ? 'badge-orange'
      : 'badge-neutral'

  return <span className={`badge ${toneClass}`}>{children}</span>
}

export function VerificationBadge({ value }: { value?: string }) {
  const normalized = (value || '').toLowerCase()
  if (normalized.includes('verified') || normalized.includes('reviewed') || normalized === 'human reviewed') {
    return (
      <StatusBadge tone="verified">
        <ShieldCheck size={12} />
        <span>{value || 'Verified'}</span>
      </StatusBadge>
    )
  }
  if (normalized.includes('passage') || normalized.includes('extracted')) {
    return (
      <StatusBadge tone="orange">
        <FileText size={12} />
        <span>{value || 'Extracted passage'}</span>
      </StatusBadge>
    )
  }
  if (normalized.includes('metadata') || normalized.includes('pending') || normalized.includes('warning')) {
    return (
      <StatusBadge tone="warning">
        <CircleAlert size={12} />
        <span>{value || 'Metadata only'}</span>
      </StatusBadge>
    )
  }
  return (
    <StatusBadge tone="unverified">
      <CircleAlert size={12} />
      <span>{value || 'Unverified'}</span>
    </StatusBadge>
  )
}

export function EvidenceBadge({ value }: { value?: string }) {
  const normalized = (value || '').toLowerCase()
  if (normalized.includes('experiment')) {
    return (
      <StatusBadge tone="verified">
        <FlaskConical size={12} />
        <span>Experimental</span>
      </StatusBadge>
    )
  }
  if (normalized.includes('simulation') || normalized.includes('model')) {
    return (
      <StatusBadge tone="warning">
        <FlaskConical size={12} />
        <span>Simulation</span>
      </StatusBadge>
    )
  }
  if (normalized.includes('abstract') || normalized.includes('bibliographic')) {
    return (
      <StatusBadge tone="neutral">
        <FileText size={12} />
        <span>Abstract Scope</span>
      </StatusBadge>
    )
  }
  return (
    <StatusBadge tone="neutral">
      <FlaskConical size={12} />
      <span>{value || 'General Evidence'}</span>
    </StatusBadge>
  )
}

export function MatchStatusBadge({ status }: { status?: string }) {
  const s = (status || '').toLowerCase()
  if (s === 'exact_match' || s === 'exact') {
    return (
      <StatusBadge tone="verified">
        <CheckCircle2 size={12} />
        <span>Exact Match</span>
      </StatusBadge>
    )
  }
  if (s === 'compatible') {
    return (
      <StatusBadge tone="verified">
        <CheckCircle2 size={12} />
        <span>Compatible</span>
      </StatusBadge>
    )
  }
  if (s === 'partial_match' || s === 'partial') {
    return (
      <StatusBadge tone="warning">
        <CircleAlert size={12} />
        <span>Partial Match</span>
      </StatusBadge>
    )
  }
  if (s === 'mismatch') {
    return (
      <StatusBadge tone="unverified">
        <XCircle size={12} />
        <span>Mismatch</span>
      </StatusBadge>
    )
  }
  return (
    <StatusBadge tone="neutral">
      <HelpCircle size={12} />
      <span>Unknown</span>
    </StatusBadge>
  )
}
