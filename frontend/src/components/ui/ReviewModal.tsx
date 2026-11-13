import { useEffect, useState } from 'react'
import {
  AlertTriangle,
  CheckCircle2,
  Clock,
  ExternalLink,
  FileCheck,
  History,
  Plus,
  RefreshCw,
  Send,
  Shield,
  X,
} from 'lucide-react'
import { api } from '../../api/client'
import type { ReviewItem } from '../../types/api'
import { StatusBadge, VerificationBadge } from './StatusBadge'

const DEMO_WRITES_DISABLED = true

interface ReviewModalProps {
  isOpen: boolean
  onClose: () => void
  initialTargetType?: string
  initialTargetId?: string
  initialNasaId?: string
}

export function ReviewModal({
  isOpen,
  onClose,
  initialTargetType = 'paper',
  initialTargetId = '',
  initialNasaId = '',
}: ReviewModalProps) {
  const [activeTab, setActiveTab] = useState<'list' | 'create' | 'history'>('list')
  const [reviews, setReviews] = useState<ReviewItem[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // Revision history state
  const [selectedReviewHistory, setSelectedReviewHistory] = useState<{
    review_id: string
    revision_count: number
    history: ReviewItem[]
  } | null>(null)
  const [historyLoading, setHistoryLoading] = useState(false)

  // Create form state
  const [targetType, setTargetType] = useState(initialTargetType)
  const [targetId, setTargetId] = useState(initialTargetId)
  const [nasaId, setNasaId] = useState(initialNasaId)
  const [status, setStatus] = useState<'pending' | 'accepted' | 'rejected' | 'needs_correction' | 'insufficient_evidence'>('accepted')
  const [reviewerId, setReviewerId] = useState('aerospace_researcher_01')
  const [reviewerNotes, setReviewerNotes] = useState('')
  const [evidenceScope, setEvidenceScope] = useState('Microgravity Flame Propagation Evidence')
  const [submitting, setSubmitting] = useState(false)

  // Edit/Revision state
  const [editingReview, setEditingReview] = useState<ReviewItem | null>(null)
  const [editStatus, setEditStatus] = useState<string>('accepted')
  const [editCorrectionNotes, setEditCorrectionNotes] = useState<string>('')
  const [editReviewerNotes, setEditReviewerNotes] = useState<string>('')
  const [patching, setPatching] = useState(false)

  useEffect(() => {
    if (isOpen) {
      void loadReviews()
      if (initialTargetId) {
        setTargetId(initialTargetId)
      }
      if (initialTargetType) {
        setTargetType(initialTargetType)
      }
      if (initialNasaId) {
        setNasaId(initialNasaId)
      }
    }
  }, [isOpen, initialTargetId, initialTargetType, initialNasaId])

  const loadReviews = async () => {
    try {
      setLoading(true)
      setError(null)
      const res = await api.getReviews({ limit: 50 })
      setReviews(res.reviews || (res as any).records || [])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch reviews ledger')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateReview = async (e: React.FormEvent) => {
    e.preventDefault()
    if (DEMO_WRITES_DISABLED) {
      setError('Review creation is disabled for the local judge demo.')
      return
    }
    if (!targetId.trim()) {
      setError('Target ID is required.')
      return
    }

    try {
      setSubmitting(true)
      setError(null)
      setSuccessMessage(null)

      const payload = {
        target_type: targetType,
        target_id: targetId.trim(),
        nasa_id: nasaId.trim() || undefined,
        status,
        reviewer_id: reviewerId.trim() || undefined,
        reviewer_notes: reviewerNotes.trim() || undefined,
        evidence_scope: evidenceScope.trim() || undefined,
      }

      const created = await api.createReview(payload)
      setSuccessMessage(`Review ${created.review_id.slice(0, 8)} successfully committed to SQLite ledger.`)
      await loadReviews()
      setActiveTab('list')
      setReviewerNotes('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to commit review')
    } finally {
      setSubmitting(false)
    }
  }

  const handleViewHistory = async (reviewId: string) => {
    try {
      setHistoryLoading(true)
      setError(null)
      const hist = await api.getReviewHistory(reviewId)
      setSelectedReviewHistory({
        review_id: hist.review_id,
        revision_count: hist.history?.length || 0,
        history: (hist.history || []) as any,
      })
      setActiveTab('history')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to retrieve revision history')
    } finally {
      setHistoryLoading(false)
    }
  }

  const handlePatchReview = async (e: React.FormEvent) => {
    e.preventDefault()
    if (DEMO_WRITES_DISABLED) {
      setError('Review revisions are disabled for the local judge demo.')
      return
    }
    if (!editingReview) return

    try {
      setPatching(true)
      setError(null)
      setSuccessMessage(null)

      const updated = await api.updateReview(editingReview.review_id, {
        status: editStatus,
        correction_notes: editCorrectionNotes.trim() || undefined,
        reviewer_notes: editReviewerNotes.trim() || undefined,
      })

      setSuccessMessage(`Review updated to revision ${updated.revision}.`)
      setEditingReview(null)
      await loadReviews()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update review')
    } finally {
      setPatching(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="drawer-scrim" onClick={onClose} style={{ zIndex: 9999 }}>
      <div
        className="editorial-modal-content"
        onClick={(e) => e.stopPropagation()}
        style={{
          width: '92%',
          maxWidth: '820px',
          maxHeight: '90vh',
          backgroundColor: '#1E1E1B',
          border: '1px solid rgba(255, 255, 255, 0.16)',
          borderRadius: '8px',
          color: '#FAF9F6',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '0 24px 64px rgba(0, 0, 0, 0.75)',
          overflow: 'hidden',
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: '18px 24px',
            borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            backgroundColor: '#151515',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <FileCheck size={20} style={{ color: '#D96C32' }} />
            <div>
              <h2 style={{ margin: 0, fontSize: '17px', fontWeight: 700, color: '#FAF9F6' }}>
                Scientific Peer Review Ledger
              </h2>
              <div style={{ fontSize: '11px', color: '#A2A299' }}>
                Persistent SQLite audit storage for human verification notes & revisions
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              color: '#A2A299',
              cursor: 'pointer',
              padding: '4px',
              display: 'flex',
              alignItems: 'center',
            }}
            aria-label="Close peer review modal"
          >
            <X size={20} />
          </button>
        </div>

        {/* Safeguard Notice */}
        <div
          style={{
            padding: '10px 24px',
            backgroundColor: 'rgba(217, 108, 50, 0.12)',
            borderBottom: '1px solid rgba(217, 108, 50, 0.25)',
            fontSize: '11px',
            color: '#D3D3CB',
            display: 'flex',
            gap: '8px',
            alignItems: 'center',
          }}
        >
          <AlertTriangle size={14} style={{ color: '#D96C32', flexShrink: 0 }} />
          <span>
            <strong>GOVERNANCE DISCLOSURE:</strong> Reviewer identities are unauthenticated in this deployment.
            Recorded peer reviews provide a transparent evidence trail but do not constitute official NASA flight clearance.
            Local judge demo write actions are disabled; existing reviews remain available for read-only inspection.
          </span>
        </div>

        {/* Nav Tabs */}
        <div
          style={{
            display: 'flex',
            borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
            backgroundColor: '#191917',
            padding: '0 24px',
          }}
        >
          <button
            onClick={() => {
              setActiveTab('list')
              setEditingReview(null)
            }}
            style={{
              padding: '12px 16px',
              fontSize: '12px',
              fontWeight: 600,
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'list' && !editingReview ? '2px solid #D96C32' : '2px solid transparent',
              color: activeTab === 'list' && !editingReview ? '#FAF9F6' : '#A2A299',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <Clock size={13} />
            <span>Active Reviews ({reviews.length})</span>
          </button>

          <button
            onClick={() => {
              setActiveTab('create')
              setEditingReview(null)
            }}
            disabled={DEMO_WRITES_DISABLED}
            style={{
              padding: '12px 16px',
              fontSize: '12px',
              fontWeight: 600,
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'create' ? '2px solid #D96C32' : '2px solid transparent',
              color: activeTab === 'create' ? '#FAF9F6' : '#A2A299',
              cursor: 'pointer',
              opacity: DEMO_WRITES_DISABLED ? 0.5 : 1,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <Plus size={13} />
            <span>Record New Review</span>
          </button>

          {selectedReviewHistory && (
            <button
              onClick={() => setActiveTab('history')}
              style={{
                padding: '12px 16px',
                fontSize: '12px',
                fontWeight: 600,
                background: 'none',
                border: 'none',
                borderBottom: activeTab === 'history' ? '2px solid #D96C32' : '2px solid transparent',
                color: activeTab === 'history' ? '#FAF9F6' : '#A2A299',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              <History size={13} />
              <span>Revision History ({selectedReviewHistory.revision_count})</span>
            </button>
          )}

          <button
            onClick={loadReviews}
            disabled={loading}
            style={{
              marginLeft: 'auto',
              background: 'none',
              border: 'none',
              color: '#A2A299',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px',
              fontSize: '11px',
            }}
            title="Refresh reviews"
          >
            <RefreshCw size={12} className={loading ? 'spin' : ''} />
            <span>Refresh</span>
          </button>
        </div>

        {/* Notifications */}
        {error && (
          <div
            style={{
              margin: '12px 24px 0',
              padding: '8px 12px',
              backgroundColor: 'rgba(217, 83, 79, 0.15)',
              border: '1px solid rgba(217, 83, 79, 0.3)',
              borderRadius: '4px',
              color: '#FF8888',
              fontSize: '12px',
            }}
          >
            {error}
          </div>
        )}

        {successMessage && (
          <div
            style={{
              margin: '12px 24px 0',
              padding: '8px 12px',
              backgroundColor: 'rgba(74, 144, 94, 0.15)',
              border: '1px solid rgba(74, 144, 94, 0.3)',
              borderRadius: '4px',
              color: '#82D898',
              fontSize: '12px',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <CheckCircle2 size={13} />
            <span>{successMessage}</span>
          </div>
        )}

        {/* Body Area */}
        <div
          style={{
            padding: '20px 24px',
            overflowY: 'auto',
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            gap: '16px',
          }}
        >
          {/* TAB 1: REVIEW LIST */}
          {activeTab === 'list' && !editingReview && (
            <>
              {loading && reviews.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '32px 0', color: '#A2A299', fontSize: '13px' }}>
                  Loading recorded peer reviews...
                </div>
              ) : reviews.length === 0 ? (
                <div
                  style={{
                    textAlign: 'center',
                    padding: '36px 20px',
                    backgroundColor: '#151515',
                    borderRadius: '6px',
                    border: '1px dashed rgba(255, 255, 255, 0.12)',
                  }}
                >
                  <FileCheck size={28} style={{ color: '#A2A299', marginBottom: '8px' }} />
                  <div style={{ fontSize: '14px', fontWeight: 600, color: '#FAF9F6', marginBottom: '4px' }}>
                    No reviews recorded yet
                  </div>
                  <div style={{ fontSize: '12px', color: '#A2A299', maxWidth: '400px', margin: '0 auto 16px' }}>
                    Record an evaluation for any paper, extracted claim, or mission brief to initialize the SQLite audit trail.
                  </div>
                  <button
                    onClick={() => setActiveTab('create')}
                    disabled={DEMO_WRITES_DISABLED}
                    className="btn btn-primary btn-sm"
                    style={{ margin: '0 auto', opacity: DEMO_WRITES_DISABLED ? 0.5 : 1 }}
                  >
                    <Plus size={14} />
                    <span>{DEMO_WRITES_DISABLED ? 'Review Writes Disabled' : 'Create First Review'}</span>
                  </button>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {reviews.map((rev) => (
                    <div
                      key={rev.review_id}
                      style={{
                        backgroundColor: '#151515',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        borderRadius: '6px',
                        padding: '14px 16px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '10px',
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
                        <div>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                            <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#D96C32', backgroundColor: 'rgba(217, 108, 50, 0.15)', padding: '2px 6px', borderRadius: '3px' }}>
                              REV #{rev.revision}
                            </span>
                            <span style={{ fontSize: '11px', color: '#A2A299', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                              {rev.target_type}
                            </span>
                            <span style={{ fontSize: '12px', fontFamily: 'monospace', color: '#FAF9F6', fontWeight: 600 }}>
                              {rev.target_id}
                            </span>
                          </div>
                          {rev.nasa_id && (
                            <div style={{ fontSize: '11px', color: '#B98555' }}>
                              NASA Identifier: {rev.nasa_id}
                            </div>
                          )}
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <StatusBadge tone={rev.status === 'accepted' ? 'verified' : rev.status === 'needs_correction' ? 'warning' : 'neutral'}>
                            {rev.status.toUpperCase()}
                          </StatusBadge>
                        </div>
                      </div>

                      {rev.reviewer_notes && (
                        <div
                          style={{
                            fontSize: '12px',
                            color: '#D3D3CB',
                            lineHeight: 1.5,
                            backgroundColor: 'rgba(255, 255, 255, 0.03)',
                            padding: '8px 12px',
                            borderRadius: '4px',
                            borderLeft: '2px solid #D96C32',
                          }}
                        >
                          &ldquo;{rev.reviewer_notes}&rdquo;
                        </div>
                      )}

                      {rev.correction_notes && (
                        <div
                          style={{
                            fontSize: '11px',
                            color: '#E0A96D',
                            lineHeight: 1.4,
                            padding: '6px 10px',
                            backgroundColor: 'rgba(217, 108, 50, 0.08)',
                            borderRadius: '4px',
                          }}
                        >
                          <strong>Correction Note:</strong> {rev.correction_notes}
                        </div>
                      )}

                      <div
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          alignItems: 'center',
                          paddingTop: '8px',
                          borderTop: '1px solid rgba(255, 255, 255, 0.05)',
                          fontSize: '11px',
                          color: '#A2A299',
                          flexWrap: 'wrap',
                          gap: '8px',
                        }}
                      >
                        <div>
                          <span>Reviewer: </span>
                          <span style={{ color: '#FAF9F6' }}>{rev.reviewer_id || 'Anonymous Researcher'}</span>
                          <span style={{ marginLeft: '12px' }}>Created: </span>
                          <span>{new Date(rev.created_at).toLocaleDateString()}</span>
                        </div>

                        <div style={{ display: 'flex', gap: '8px' }}>
                          <button
                            onClick={() => handleViewHistory(rev.review_id)}
                            style={{
                              background: 'none',
                              border: '1px solid rgba(255, 255, 255, 0.15)',
                              borderRadius: '3px',
                              color: '#D3D3CB',
                              fontSize: '11px',
                              padding: '3px 8px',
                              cursor: 'pointer',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '4px',
                            }}
                          >
                            <History size={11} />
                            <span>Audit History</span>
                          </button>

                          <button
                            onClick={() => {
                              setEditingReview(rev)
                              setEditStatus(rev.status)
                              setEditReviewerNotes(rev.reviewer_notes || '')
                              setEditCorrectionNotes(rev.correction_notes || '')
                            }}
                            disabled={DEMO_WRITES_DISABLED}
                            style={{
                              background: 'none',
                              border: '1px solid #D96C32',
                              borderRadius: '3px',
                              color: '#D96C32',
                              fontSize: '11px',
                              padding: '3px 8px',
                              cursor: 'pointer',
                              opacity: DEMO_WRITES_DISABLED ? 0.5 : 1,
                            }}
                          >
                            Revise
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}

          {/* TAB 2: CREATE REVIEW FORM */}
          {activeTab === 'create' && !editingReview && (
            <form onSubmit={handleCreateReview} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                    TARGET TYPE *
                  </label>
                  <select
                    value={targetType}
                    onChange={(e) => setTargetType(e.target.value)}
                    style={{
                      width: '100%',
                      backgroundColor: '#151515',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '4px',
                      color: '#FAF9F6',
                      padding: '8px 10px',
                      fontSize: '12px',
                    }}
                  >
                    <option value="paper">Paper (NASA Document)</option>
                    <option value="claim">Claim (Extracted Finding)</option>
                    <option value="structured_finding">Structured Finding</option>
                    <option value="comparison">Comparison Pair</option>
                    <option value="conflict">Source Conflict</option>
                    <option value="research_gap">Research Gap</option>
                    <option value="mission_brief">Mission Brief</option>
                  </select>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                    TARGET IDENTIFIER *
                  </label>
                  <input
                    type="text"
                    value={targetId}
                    onChange={(e) => setTargetId(e.target.value)}
                    placeholder="e.g. 20150019483 or claim-01"
                    required
                    style={{
                      width: '100%',
                      backgroundColor: '#151515',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '4px',
                      color: '#FAF9F6',
                      padding: '8px 10px',
                      fontSize: '12px',
                    }}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                    NASA ID (OPTIONAL)
                  </label>
                  <input
                    type="text"
                    value={nasaId}
                    onChange={(e) => setNasaId(e.target.value)}
                    placeholder="e.g. 20150019483"
                    style={{
                      width: '100%',
                      backgroundColor: '#151515',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '4px',
                      color: '#FAF9F6',
                      padding: '8px 10px',
                      fontSize: '12px',
                    }}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                    REVIEW DECISION / STATUS *
                  </label>
                  <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value as any)}
                    style={{
                      width: '100%',
                      backgroundColor: '#151515',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '4px',
                      color: '#FAF9F6',
                      padding: '8px 10px',
                      fontSize: '12px',
                    }}
                  >
                    <option value="accepted">Accepted (Review State Only)</option>
                    <option value="pending">Pending Further Analysis</option>
                    <option value="needs_correction">Needs Correction</option>
                    <option value="rejected">Rejected (Insufficient Provenance)</option>
                    <option value="insufficient_evidence">Insufficient Experimental Data</option>
                  </select>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                    REVIEWER IDENTIFIER
                  </label>
                  <input
                    type="text"
                    value={reviewerId}
                    onChange={(e) => setReviewerId(e.target.value)}
                    placeholder="e.g. investigator_name"
                    style={{
                      width: '100%',
                      backgroundColor: '#151515',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '4px',
                      color: '#FAF9F6',
                      padding: '8px 10px',
                      fontSize: '12px',
                    }}
                  />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                    EVIDENCE SCOPE
                  </label>
                  <input
                    type="text"
                    value={evidenceScope}
                    onChange={(e) => setEvidenceScope(e.target.value)}
                    placeholder="e.g. Microgravity Flame Spread Findings"
                    style={{
                      width: '100%',
                      backgroundColor: '#151515',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '4px',
                      color: '#FAF9F6',
                      padding: '8px 10px',
                      fontSize: '12px',
                    }}
                  />
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                  SCIENTIFIC REVIEWER NOTES *
                </label>
                <textarea
                  value={reviewerNotes}
                  onChange={(e) => setReviewerNotes(e.target.value)}
                  placeholder="Record your verification notes, scientific qualifications, experimental limitations, and boundary conditions..."
                  rows={4}
                  style={{
                    width: '100%',
                    backgroundColor: '#151515',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '4px',
                    color: '#FAF9F6',
                    padding: '8px 10px',
                    fontSize: '12px',
                    resize: 'vertical',
                    lineHeight: 1.5,
                  }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '6px' }}>
                <button
                  type="button"
                  onClick={() => setActiveTab('list')}
                  className="btn btn-secondary btn-sm"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting || DEMO_WRITES_DISABLED}
                  className="btn btn-primary btn-sm"
                >
                  <Send size={13} />
                  <span>{DEMO_WRITES_DISABLED ? 'Review Writes Disabled for Local Demo' : submitting ? 'Recording to Ledger...' : 'Commit Review (POST /research/reviews)'}</span>
                </button>
              </div>
            </form>
          )}

          {/* EDIT/REVISE REVIEW FORM */}
          {editingReview && (
            <form onSubmit={handlePatchReview} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div style={{ backgroundColor: '#151515', padding: '12px 14px', borderRadius: '4px', border: '1px solid rgba(255, 255, 255, 0.1)' }}>
                <span style={{ fontSize: '11px', color: '#D96C32', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
                  REVISING REVIEW {editingReview.review_id.slice(0, 8)} (CURRENT REVISION #{editingReview.revision})
                </span>
                <div style={{ fontSize: '12px', color: '#FAF9F6' }}>
                  Target: <strong>{editingReview.target_type}</strong> / ID: <code>{editingReview.target_id}</code>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                  UPDATED STATUS *
                </label>
                <select
                  value={editStatus}
                  onChange={(e) => setEditStatus(e.target.value)}
                  style={{
                    width: '100%',
                    backgroundColor: '#151515',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '4px',
                    color: '#FAF9F6',
                    padding: '8px 10px',
                    fontSize: '12px',
                  }}
                >
                  <option value="accepted">Accepted (Review State Only)</option>
                  <option value="pending">Pending Further Analysis</option>
                  <option value="needs_correction">Needs Correction</option>
                  <option value="rejected">Rejected</option>
                  <option value="insufficient_evidence">Insufficient Evidence</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                  CORRECTION NOTES
                </label>
                <input
                  type="text"
                  value={editCorrectionNotes}
                  onChange={(e) => setEditCorrectionNotes(e.target.value)}
                  placeholder="Detail the corrections or amendments made in this revision..."
                  style={{
                    width: '100%',
                    backgroundColor: '#151515',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '4px',
                    color: '#FAF9F6',
                    padding: '8px 10px',
                    fontSize: '12px',
                  }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', color: '#A2A299', marginBottom: '4px', fontWeight: 600 }}>
                  AMENDED REVIEWER NOTES
                </label>
                <textarea
                  value={editReviewerNotes}
                  onChange={(e) => setEditReviewerNotes(e.target.value)}
                  rows={3}
                  style={{
                    width: '100%',
                    backgroundColor: '#151515',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '4px',
                    color: '#FAF9F6',
                    padding: '8px 10px',
                    fontSize: '12px',
                  }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                <button
                  type="button"
                  onClick={() => setEditingReview(null)}
                  className="btn btn-secondary btn-sm"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={patching || DEMO_WRITES_DISABLED}
                  className="btn btn-primary btn-sm"
                >
                  <Send size={13} />
                  <span>{DEMO_WRITES_DISABLED ? 'Review Writes Disabled for Local Demo' : patching ? 'Updating Ledger...' : 'Commit Revision (PATCH /research/reviews/{id})'}</span>
                </button>
              </div>
            </form>
          )}

          {/* TAB 3: REVISION HISTORY */}
          {activeTab === 'history' && selectedReviewHistory && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '13px', fontWeight: 600, color: '#FAF9F6' }}>
                  Audit History for Review: <code>{selectedReviewHistory.review_id.slice(0, 12)}...</code>
                </span>
                <span style={{ fontSize: '11px', color: '#A2A299' }}>
                  {selectedReviewHistory.revision_count} Total Revision(s) Recorded
                </span>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {selectedReviewHistory.history.map((h, i) => (
                  <div
                    key={i}
                    style={{
                      padding: '12px 14px',
                      backgroundColor: '#151515',
                      border: '1px solid rgba(255, 255, 255, 0.08)',
                      borderRadius: '4px',
                      fontSize: '12px',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                      <span style={{ fontWeight: 600, color: '#D96C32' }}>Revision #{h.revision}</span>
                      <StatusBadge tone={h.status === 'accepted' ? 'verified' : 'neutral'}>
                        {h.status}
                      </StatusBadge>
                    </div>
                    {h.reviewer_notes && (
                      <div style={{ color: '#D3D3CB', marginBottom: '4px' }}>
                        Notes: &ldquo;{h.reviewer_notes}&rdquo;
                      </div>
                    )}
                    {h.correction_notes && (
                      <div style={{ color: '#E0A96D', fontSize: '11px', marginBottom: '4px' }}>
                        Correction: {h.correction_notes}
                      </div>
                    )}
                    <div style={{ fontSize: '10px', color: '#686861', display: 'flex', justifyContent: 'space-between' }}>
                      <span>Reviewer: {h.reviewer_id || 'anonymous'}</span>
                      <span>Recorded: {new Date(h.created_at).toLocaleString()}</span>
                    </div>
                  </div>
                ))}
              </div>

              <button
                type="button"
                onClick={() => setActiveTab('list')}
                className="btn btn-secondary btn-sm"
                style={{ alignSelf: 'flex-start' }}
              >
                Back to Review List
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
