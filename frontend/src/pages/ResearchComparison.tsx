import { useEffect, useState } from 'react'
import {
  AlertCircle,
  ArrowRight,
  CircleHelp,
  Compass,
  ExternalLink,
  FileQuestion,
  GitCompare,
  HelpCircle,
  Layers,
  Search,
  ShieldAlert,
} from 'lucide-react'
import { api } from '../api/client'
import type { ComparisonPair, ResearchComparisonResponse } from '../types/api'
import { PageMediaHeader } from '../components/ui/PageMediaHeader'
import { SectionHeader } from '../components/ui/SectionHeader'
import { StatCard } from '../components/ui/StatCard'
import { StatusBadge, MatchStatusBadge, EvidenceBadge } from '../components/ui/StatusBadge'
import { EditorialCard } from '../components/ui/GlassCard'
import { ErrorState, LoadingState, EmptyState } from '../components/ui/FeedbackStates'

export default function ResearchComparison() {
  const [query, setQuery] = useState('PMMA flame spread oxygen concentration')
  const [limit, setLimit] = useState(6)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [comparisonData, setComparisonData] = useState<ResearchComparisonResponse | null>(null)
  const [selectedPairIndex, setSelectedPairIndex] = useState(0)

  const fetchComparison = async (targetQuery = query) => {
    if (!targetQuery || targetQuery.trim().length < 2) return
    setLoading(true)
    setError(null)
    try {
      const res = await api.getResearchComparison(targetQuery, limit)
      setComparisonData(res)
      setSelectedPairIndex(0)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate research comparison.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void fetchComparison()
  }, [limit])

  const pairs: ComparisonPair[] = comparisonData?.comparison?.condition_comparisons || []
  const activePair: ComparisonPair | undefined = pairs[selectedPairIndex]

  const formatValues = (vals: Array<{ value: unknown; raw_value: unknown; unit?: string | null }>) => {
    if (!vals || vals.length === 0) return <span style={{ color: '#8C8C85', fontStyle: 'italic' }}>Not reported</span>
    return vals.map((v, i) => (
      <span key={i} className="cell-mono">
        {String(v.value || v.raw_value)} {v.unit ? v.unit : ''}
      </span>
    ))
  }

  return (
    <div className="page-enter">
      {/* 1. Page Header with genuine NASA photography */}
      <PageMediaHeader
        image="/media/images/skylab-earth-orbit.jpg"
        alt="Skylab space station cluster in Earth orbit"
        credit="NASA · sl4-143-4707 (Official NASA Earth-orbit photograph)"
      >
        <SectionHeader
          dark
          eyebrow="CROSS-STUDY CONDITION COMPARISON"
          title="Pairwise Scientific Parameter Comparison"
          detail="Conservative parameter matching across 9 condition dimensions. Compares explicit value and unit signatures without inferring equivalence."
          action={
            <StatusBadge tone="orange">
              <GitCompare size={13} />
              <span>9-Dimension Condition Matrix</span>
            </StatusBadge>
          }
        />
      </PageMediaHeader>

      {/* 2. Scientific Disclosure Banner */}
      <div className="safeguard-banner">
        <ShieldAlert size={16} style={{ color: '#D96C32', flexShrink: 0 }} />
        <span>
          <strong>NON-EQUIVALENCE SAFEGUARD:</strong> No unit conversions, material equivalence, or causal equivalence is assumed.
          Unreported parameters remain strictly <em>unknown</em>. Differences represent condition mismatches, not verified scientific contradictions.
        </span>
      </div>

      {/* 3. Query Bar */}
      <div className="search-workspace-box">
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <div className="search-field">
            <Search size={16} style={{ color: '#686861' }} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') void fetchComparison()
              }}
              placeholder="Query comparison domain (e.g. 'PMMA flame spread', 'oxygen concentration')..."
            />
          </div>
          <button className="btn btn-primary" onClick={() => fetchComparison()} disabled={loading}>
            <span>{loading ? 'Comparing...' : 'Compare Studies'}</span>
          </button>
        </div>

        <div className="filter-bar">
          <span>MAX SOURCE PAPERS:</span>
          <select value={limit} onChange={(e) => setLimit(Number(e.target.value))}>
            <option value={4}>4 Documents (up to 6 pairs)</option>
            <option value={6}>6 Documents (up to 15 pairs)</option>
            <option value={8}>8 Documents (up to 28 pairs)</option>
          </select>

          {pairs.length > 0 && (
            <span style={{ marginLeft: 'auto', color: '#686861', fontFamily: 'monospace' }}>
              {pairs.length} pairwise study comparison(s) formed
            </span>
          )}
        </div>
      </div>

      {error && (
        <ErrorState
          title="Comparison Engine Notice"
          message={error}
          onRetry={() => fetchComparison()}
        />
      )}

      {loading && <LoadingState message="Extracting condition dimensions and building comparison matrix..." />}

      {/* 4. Comparison Pair Selector */}
      {comparisonData && !loading && pairs.length > 0 && (
        <div style={{ marginBottom: '24px' }}>
          <EditorialCard variant="dark">
            <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '16px' }}>
              <div>
                <span className="eyebrow eyebrow-dark">STUDY PAIR SELECTION</span>
                <h3 style={{ margin: 0, fontSize: '16px', color: '#FFFFFF' }}>
                  Select Study Pair to Inspect
                </h3>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span style={{ fontSize: '11px', color: '#A2A299', fontFamily: 'monospace' }}>PAIR:</span>
                <select
                  value={selectedPairIndex}
                  onChange={(e) => setSelectedPairIndex(Number(e.target.value))}
                  style={{
                    backgroundColor: '#22221F',
                    color: '#FAF9F6',
                    border: '1px solid rgba(255,255,255,0.2)',
                    padding: '8px 12px',
                    borderRadius: '4px',
                    fontSize: '12px',
                    fontFamily: 'monospace',
                  }}
                >
                  {pairs.map((p, idx) => (
                    <option key={idx} value={idx}>
                      #{idx + 1}: {p.first_source?.nasa_id || 'Study A'} vs {p.second_source?.nasa_id || 'Study B'} ({p.overall_status.toUpperCase()})
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </EditorialCard>
        </div>
      )}

      {/* 5. Side-by-Side Study Cards & Condition Matrix */}
      {activePair && !loading && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Side by side study cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
            {/* Study A */}
            <EditorialCard variant="charcoal">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span className="nasa-id-pill nasa-id-pill-dark">
                  STUDY A: {activePair.first_source?.nasa_id}
                </span>
                <EvidenceBadge value={activePair.first_source?.evidence_classification} />
              </div>
              <h4 style={{ margin: '0 0 10px', fontSize: '15px', color: '#FFFFFF', lineHeight: 1.4 }}>
                {activePair.first_source?.source_title}
              </h4>
              <div style={{ fontSize: '11px', color: '#A2A299', display: 'flex', gap: '12px' }}>
                <span>Type: {activePair.first_source?.source_type}</span>
                <span>Review: {activePair.first_source?.review_status}</span>
              </div>
              {activePair.first_source?.source_url && (
                <a
                  href={activePair.first_source.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: '#D96C32', fontSize: '11px', marginTop: '10px' }}
                >
                  <span>Citation URL</span>
                  <ExternalLink size={11} />
                </a>
              )}
            </EditorialCard>

            {/* Study B */}
            <EditorialCard variant="charcoal">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span className="nasa-id-pill nasa-id-pill-dark">
                  STUDY B: {activePair.second_source?.nasa_id}
                </span>
                <EvidenceBadge value={activePair.second_source?.evidence_classification} />
              </div>
              <h4 style={{ margin: '0 0 10px', fontSize: '15px', color: '#FFFFFF', lineHeight: 1.4 }}>
                {activePair.second_source?.source_title}
              </h4>
              <div style={{ fontSize: '11px', color: '#A2A299', display: 'flex', gap: '12px' }}>
                <span>Type: {activePair.second_source?.source_type}</span>
                <span>Review: {activePair.second_source?.review_status}</span>
              </div>
              {activePair.second_source?.source_url && (
                <a
                  href={activePair.second_source.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: '#D96C32', fontSize: '11px', marginTop: '10px' }}
                >
                  <span>Citation URL</span>
                  <ExternalLink size={11} />
                </a>
              )}
            </EditorialCard>
          </div>

          {/* Condition Matrix Table */}
          <div className="dark-panel" style={{ padding: '0', overflow: 'hidden' }}>
            <div style={{ padding: '18px 20px', borderBottom: '1px solid var(--border-dark)', display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', gap: '12px' }}>
              <div>
                <span className="eyebrow eyebrow-dark">9 CONDITION DIMENSIONS</span>
                <h3 style={{ margin: 0, fontSize: '17px', color: '#FFFFFF' }}>
                  Condition Comparison Matrix
                </h3>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '11px', color: '#A2A299', fontFamily: 'monospace' }}>OVERALL ALIGNMENT:</span>
                <MatchStatusBadge status={activePair.overall_status} />
              </div>
            </div>

            <div style={{ overflowX: 'auto' }}>
              <table className="comparison-matrix-table">
                <thead>
                  <tr>
                    <th style={{ width: '22%' }}>Dimension</th>
                    <th style={{ width: '30%' }}>Study A ({activePair.first_source?.nasa_id})</th>
                    <th style={{ width: '30%' }}>Study B ({activePair.second_source?.nasa_id})</th>
                    <th style={{ width: '18%' }}>Match Status</th>
                  </tr>
                </thead>
                <tbody>
                  {activePair.condition_comparisons?.map((field, fIdx) => (
                    <tr key={fIdx}>
                      <td style={{ fontWeight: 600, color: '#FAF9F6', textTransform: 'capitalize' }}>
                        {field.dimension.replace(/_/g, ' ')}
                      </td>
                      <td>{formatValues(field.first_source_values)}</td>
                      <td>{formatValues(field.second_source_values)}</td>
                      <td>
                        <MatchStatusBadge status={field.status} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div style={{ padding: '14px 24px', backgroundColor: 'rgba(0,0,0,0.3)', borderTop: '1px solid var(--border-dark)', fontSize: '11px', color: '#A2A299' }}>
              <strong>Rationale:</strong> {activePair.comparison_rationale}
            </div>
          </div>

          {/* 6. Research Gaps & Suggested Questions */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
            {/* Research Gaps */}
            <EditorialCard variant="dark">
              <div className="eyebrow eyebrow-dark">EVIDENCE GAPS</div>
              <h3 style={{ margin: '0 0 12px', fontSize: '16px', color: '#FFFFFF' }}>
                Unresolved Parameters
              </h3>
              {activePair.missing_information && activePair.missing_information.length > 0 ? (
                <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '12px', color: '#D3D3CB', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {activePair.missing_information.map((item, i) => (
                    <li key={i} style={{ textTransform: 'capitalize' }}>
                      {item.replace(/_/g, ' ')} unrecorded or partially documented
                    </li>
                  ))}
                </ul>
              ) : (
                <p style={{ margin: 0, fontSize: '12px', color: '#A2A299' }}>
                  No missing parameters identified for this pair.
                </p>
              )}
            </EditorialCard>

            {/* Suggested Follow-up Questions */}
            <EditorialCard variant="charcoal">
              <div className="eyebrow eyebrow-dark">FOLLOW-UP RESEARCH INQUIRIES</div>
              <h3 style={{ margin: '0 0 12px', fontSize: '16px', color: '#FFFFFF' }}>
                Next Verification Questions
              </h3>
              {comparisonData?.suggested_research_questions && comparisonData.suggested_research_questions.length > 0 ? (
                <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '12px', color: '#D3D3CB', display: 'flex', flexDirection: 'column', gap: '8px', lineHeight: 1.4 }}>
                  {comparisonData.suggested_research_questions.map((q) => (
                    <li key={`${q.question}-${q.gap_ids.join(',')}`}>{q.question}</li>
                  ))}
                </ul>
              ) : (
                <p style={{ margin: 0, fontSize: '12px', color: '#A2A299' }}>
                  No automated follow-up questions generated.
                </p>
              )}
            </EditorialCard>
          </div>
        </div>
      )}

      {comparisonData && !loading && pairs.length === 0 && (
        <EmptyState
          title="Fewer than two studies retrieved"
          message="Comparison requires at least two distinct documents matching the query. Try broader search terms."
        />
      )}
    </div>
  )
}
