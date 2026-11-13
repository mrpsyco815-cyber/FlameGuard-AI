import { useEffect, useState } from 'react'
import {
  AlertTriangle,
  BookOpen,
  ChevronDown,
  FileCheck2,
  FileQuestion,
  FlaskConical,
  GitBranch,
  Layers,
  Search,
  ShieldAlert,
  ShieldCheck,
} from 'lucide-react'
import { api } from '../api/client'
import type { PaperInsight, ResearchInsightsResponse } from '../types/api'
import { PageMediaHeader } from '../components/ui/PageMediaHeader'
import { SectionHeader } from '../components/ui/SectionHeader'
import { StatCard } from '../components/ui/StatCard'
import { StatusBadge, VerificationBadge, EvidenceBadge } from '../components/ui/StatusBadge'
import { EditorialCard } from '../components/ui/GlassCard'
import { ErrorState, LoadingState, EmptyState } from '../components/ui/FeedbackStates'

export default function ResearchInsights() {
  const [query, setQuery] = useState('oxygen concentration PMMA flame spread')
  const [limit, setLimit] = useState(6)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [insightsData, setInsightsData] = useState<ResearchInsightsResponse | null>(null)
  const [openPaperIndex, setOpenPaperIndex] = useState<number>(0)

  const fetchInsights = async (targetQuery = query) => {
    if (!targetQuery || targetQuery.trim().length < 2) return
    setLoading(true)
    setError(null)
    try {
      const res = await api.getResearchInsights(targetQuery, limit)
      setInsightsData(res)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to retrieve research insights.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void fetchInsights()
  }, [limit])

  return (
    <div className="page-enter">
      {/* 1. Page Header with genuine NASA photography */}
      <PageMediaHeader
        image="/media/images/solid-combustion-experiment.jpg"
        alt="NASA astronaut services combustion research components"
        credit="NASA · iss071e414661 (Solid Combustion Experiment Module context)"
      >
        <SectionHeader
          dark
          eyebrow="EXTRACTIVE RESEARCH INTELLIGENCE"
          title="Section-Linked Scientific Insights"
          detail="Synthesizing structured claims, reported condition values, and cross-study conflict intelligence with complete provenance."
          action={
            <StatusBadge tone="orange">
              <FlaskConical size={13} />
              <span>Extractive Claim Synthesis</span>
            </StatusBadge>
          }
        />
      </PageMediaHeader>

      {/* 2. Scientific Disclosure Banner */}
      <div className="safeguard-banner">
        <ShieldAlert size={16} style={{ color: '#D96C32', flexShrink: 0 }} />
        <span>
          <strong>CONSERVATIVE SYNTHESIS RULE:</strong> All claims below are extractive and source-linked; they are not independently scientifically verified.
          Simulations are kept distinct from experimental measurements. Different papers are never assumed to represent independent runs.
        </span>
      </div>

      {/* 3. Search & Control Bar */}
      <div className="search-workspace-box">
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <div className="search-field">
            <Search size={16} style={{ color: '#686861' }} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') void fetchInsights()
              }}
              placeholder="Query research topic (e.g. 'oxygen concentration and flame spread', 'PMMA')..."
            />
          </div>
          <button
            className="btn btn-primary"
            onClick={() => fetchInsights()}
            disabled={loading}
          >
            <span>{loading ? 'Synthesizing...' : 'Build Insights'}</span>
          </button>
        </div>

        <div className="filter-bar">
          <span>LIMIT PAPERS:</span>
          <select value={limit} onChange={(e) => setLimit(Number(e.target.value))}>
            <option value={4}>4 Documents</option>
            <option value={6}>6 Documents</option>
            <option value={10}>10 Documents</option>
          </select>

          {insightsData && (
            <span style={{ marginLeft: 'auto', color: '#686861', fontFamily: 'monospace' }}>
              Retrieved {insightsData.evidence?.paper_count || 0} papers · {insightsData.evidence?.claim_count || 0} extracted claims
            </span>
          )}
        </div>
      </div>

      {error && (
        <ErrorState
          title="Insights API Notice"
          message={error}
          onRetry={() => fetchInsights()}
        />
      )}

      {loading && <LoadingState message="Extracting section-aware claims and condition values..." />}

      {/* 4. Real Stats Overview */}
      {insightsData && !loading && (
        <div className="stat-grid">
          <StatCard
            label="Analyzed Sources"
            value={insightsData.evidence?.paper_count || 0}
            detail="Source documents processed"
            icon={BookOpen}
            highlight
          />
          <StatCard
            label="Extracted Claims"
            value={insightsData.evidence?.claim_count || 0}
            detail="Pattern-identified statements"
            icon={FileCheck2}
          />
          <StatCard
            label="Detected Conflicts"
            value={insightsData.conflict_report?.count || 0}
            detail="Potential condition divergences"
            icon={GitBranch}
          />
          <StatCard
            label="Scientific Status"
            value="Unverified"
            detail="Heuristic extraction only"
            icon={ShieldAlert}
          />
        </div>
      )}

      {/* 5. Main Layout: Papers/Claims vs Conservative Synthesis Side Panel */}
      {insightsData && !loading && (
        <div className="responsive-two-column-split">
          {/* Left Column: Source Papers & Claims Accordion */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <SectionHeader
              eyebrow="EXTRACTED SOURCE PAPERS"
              title="Paper Findings & Claim Provenance"
              detail="Click to expand paper claims and structured condition parameters"
            />

            {insightsData.evidence?.papers?.length === 0 ? (
              <EmptyState
                title="No papers found for this query"
                message="Try a broader scientific keyword like 'combustion' or 'oxygen'."
              />
            ) : (
              insightsData.evidence?.papers?.map((paper: PaperInsight, idx: number) => {
                const isOpen = openPaperIndex === idx
                return (
                  <div
                    key={`${paper.document_id || 'paper'}-${paper.nasa_id || 'unknown'}-${idx}`}
                    className="research-card"
                    style={{ padding: '0', overflow: 'hidden' }}
                  >
                    {/* Accordion Header */}
                    <div
                      onClick={() => setOpenPaperIndex(isOpen ? -1 : idx)}
                      style={{
                        padding: '18px 22px',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        backgroundColor: isOpen ? '#FAF9F4' : '#FFFFFF',
                        borderBottom: isOpen ? '1px solid var(--border-light)' : 'none',
                      }}
                    >
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span className="nasa-id-pill">NASA ID: {paper.nasa_id || paper.document_id}</span>
                          <EvidenceBadge value={paper.evidence_classification} />
                          <VerificationBadge value={paper.review_status} />
                        </div>
                        <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 600, color: '#171715' }}>
                          {paper.source_title}
                        </h3>
                      </div>

                      <ChevronDown
                        size={18}
                        style={{
                          transform: isOpen ? 'rotate(180deg)' : 'none',
                          transition: 'transform 0.2s ease',
                          color: '#686861',
                          flexShrink: 0,
                        }}
                      />
                    </div>

                    {/* Accordion Body */}
                    {isOpen && (
                      <div style={{ padding: '20px 22px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {/* Claims list */}
                        <div>
                          <strong style={{ display: 'block', fontSize: '11px', color: '#686861', fontFamily: 'monospace', textTransform: 'uppercase', marginBottom: '8px' }}>
                            Extracted Scientific Claims ({paper.claims?.length || 0})
                          </strong>
                          {paper.claims && paper.claims.length > 0 ? (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                              {paper.claims.map((claim, cIdx) => (
                                <div key={cIdx} className="excerpt-box">
                                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', color: '#D96C32', fontFamily: 'monospace', marginBottom: '4px' }}>
                                    <span>Section: {claim.section_name || 'unclassified'}</span>
                                    {claim.page_numbers && claim.page_numbers.length > 0 && (
                                      <span>Page: {claim.page_numbers.join(', ')}</span>
                                    )}
                                  </div>
                                  <div>&ldquo;{claim.claim_text}&rdquo;</div>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <div style={{ fontSize: '12px', color: '#A2A299', fontStyle: 'italic' }}>
                              No discrete claims parsed in this section.
                            </div>
                          )}
                        </div>

                        {/* Provenance Metadata */}
                        <div style={{ borderTop: '1px solid var(--border-light)', paddingTop: '12px', display: 'flex', gap: '16px', fontSize: '11px', color: '#686861', fontFamily: 'monospace' }}>
                          <span>Type: {paper.source_type}</span>
                          <span>Verified: {paper.scientific_findings_verified ? 'Yes' : 'Pending Review'}</span>
                          {paper.provenance?.page_numbers && paper.provenance.page_numbers.length > 0 && (
                            <span>Pages: {paper.provenance.page_numbers.join(', ')}</span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )
              })
            )}
          </div>

          {/* Right Column: Conservative Synthesis & Limitations Panel */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <EditorialCard variant="dark">
              <div className="eyebrow eyebrow-dark">CONSERVATIVE SYNTHESIS</div>
              <h3 style={{ margin: '0 0 10px', fontSize: '18px', color: '#FFFFFF' }}>
                Operational Recommendation
              </h3>
              <div style={{ padding: '14px', backgroundColor: 'rgba(217,108,50,0.12)', borderLeft: '3px solid #D96C32', borderRadius: '0 4px 4px 0', marginBottom: '16px' }}>
                <span style={{ fontSize: '12.5px', color: '#FAF9F6', fontWeight: 600, lineHeight: 1.5, display: 'block' }}>
                  {insightsData.recommendation}
                </span>
              </div>
              <p style={{ fontSize: '12px', color: '#A2A299', lineHeight: 1.5 }}>
                AeroGuard AI adheres to strict aerospace engineering safeguards. It will not synthesize speculative safety envelopes from non-verified textual evidence.
              </p>
            </EditorialCard>

            <EditorialCard variant="charcoal">
              <div className="eyebrow eyebrow-dark">SCIENTIFIC LIMITATIONS</div>
              <h3 style={{ margin: '0 0 12px', fontSize: '16px', color: '#FFFFFF' }}>
                Uncertainty Boundary
              </h3>
              <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '11.5px', color: '#D3D3CB', display: 'flex', flexDirection: 'column', gap: '8px', lineHeight: 1.5 }}>
                {insightsData.limitations?.map((lim, lIdx) => (
                  <li key={lIdx}>{lim}</li>
                ))}
              </ul>
            </EditorialCard>

            {insightsData.conflict_report && insightsData.conflict_report.count > 0 && (
              <EditorialCard variant="charcoal">
                <div className="eyebrow eyebrow-dark">POTENTIAL CONFLICTS</div>
                <h3 style={{ margin: '0 0 10px', fontSize: '16px', color: '#FFFFFF' }}>
                  Cross-Study Divergences
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {insightsData.conflict_report.conflicts?.map((c, cIdx) => (
                    <div key={cIdx} style={{ padding: '8px 10px', backgroundColor: 'rgba(0,0,0,0.3)', borderRadius: '4px', fontSize: '11px', color: '#FAF9F6' }}>
                      <b>{c.topic || 'Divergence'}</b>
                      <p style={{ margin: '4px 0 0', color: '#A2A299' }}>{c.description}</p>
                    </div>
                  ))}
                </div>
              </EditorialCard>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
