import { Loader2 } from 'lucide-react'

export function LoadingState({ message = 'Loading evidence from backend...' }: { message?: string }) {
  return (
    <div className="loading-box" role="status">
      <Loader2 size={24} className="animate-spin" style={{ color: '#D96C32' }} />
      <span>{message}</span>
    </div>
  )
}

export function ErrorState({
  title = 'API Communication Error',
  message,
  onRetry,
}: {
  title?: string
  message: string
  onRetry?: () => void
}) {
  return (
    <div className="error-box" role="alert">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
        <strong style={{ fontSize: '13px', fontWeight: 700 }}>{title}</strong>
        {onRetry && (
          <button className="btn btn-secondary btn-sm" onClick={onRetry}>
            Retry Request
          </button>
        )}
      </div>
      <p style={{ margin: 0, lineHeight: 1.5 }}>{message}</p>
    </div>
  )
}

export function EmptyState({
  title = 'No records found',
  message = 'Try modifying your search terms or filter criteria.',
}: {
  title?: string
  message?: string
}) {
  return (
    <div className="empty-box">
      <h4>{title}</h4>
      <p>{message}</p>
    </div>
  )
}

