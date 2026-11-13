import { useEffect, useState } from 'react'
import {
  CheckCircle2,
  Download,
  ExternalLink,
  FileCheck2,
  FileSearch,
  Filter,
  Layers,
  Search,
  ShieldAlert,
  SlidersHorizontal,
  UploadCloud,
  X,
} from 'lucide-react'
import { api } from '../api/client'
import type {
  CombinedSearchResponse,
  EvidenceBriefItem,
  EvidenceBriefResponse,
  OnlineResearchResultItem,
  PassageSearchResultItem,
  ReviewedEvidenceItem,
} from '../types/api'
import { PageMediaHeader } from '../components/ui/PageMediaHeader'
import { SectionHeader } from '../components/ui/SectionHeader'
import { SearchInput } from '../components/ui/SearchInput'
import { EditorialCard } from '../components/ui/GlassCard'
import { EvidenceBadge, StatusBadge, VerificationBadge } from '../components/ui/StatusBadge'
import { EmptyState, ErrorState, LoadingState } from '../components/ui/FeedbackStates'
import { ReviewModal } from '../components/ui/ReviewModal'

type SearchMode = 'brief' | 'combined' | 'reviewed' | 'passages' | 'online'

const DEMO_WRITES_DISABLED = true

export default function NasaResearch() {
  const [query, setQuery] = useState('oxygen concentration flame spread')
  const [searchMode, setSearchMode] = useState<SearchMode>('brief')
  const [limit, setLimit] = useState(8)
  const [modalityFilter, setModalityFilter] = useState('all')

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Results state
  const [briefResponse, setBriefResponse] = useState<EvidenceBriefResponse | null>(null)
  const [combinedResponse, setCombinedResponse] = useState<CombinedSearchResponse | null>(null)
  const [reviewedResults, setReviewedResults] = useState<ReviewedEvidenceItem[]>([])
  const [passageResults, setPassageResults] = useState<PassageSearchResultItem[]>([])
  const [onlineResults, setOnlineResults] = useState<OnlineResearchResultItem[]>([])

  // Document ingestion state
  const [importingNasaId, setImportingNasaId] = useState<string | null>(null)
  const [importNotice, setImportNotice] = useState<{ id: string; success: boolean; message: string } | null>(null)

  // Review modal state
  const [isReviewModalOpen, setIsReviewModalOpen] = useState(false)
  const [reviewTarget, setReviewTarget] = useState<{ id: string; nasaId?: string; type: string }>({
    id: '',
    type: 'paper',
  })

  const [selectedItem, setSelectedItem] = useState<{
    id: string
    title: string
    nasaId?: string
    excerpt: string
    sourceUrl?: string
    pdfPage?: number | null
    evidenceType?: string
    verification?: string
    matchedTerms?: string[]
    score?: number
  } | null>(null)

  const executeSearch = async (targetQuery = query) => {
    if (!targetQuery || targetQuery.trim().length < 2) return

    setLoading(true)
    setError(null)

    try {
      if (searchMode === 'brief') {
        const res = await api.searchResearch(targetQuery, limit)
        setBriefResponse(res)
      } else if (searchMode === 'combined') {
        const res = await api.searchCombinedResearch(targetQuery, limit)
        setCombinedResponse(res)
      } else if (searchMode === 'reviewed') {
        const res = await api.searchEvidence(targetQuery, limit)
        setReviewedResults(res.results || [])
      } else if (searchMode === 'passages') {
        const res = await api.searchPassages({ q: targetQuery, limit })
        setPassageResults(res.results || [])
      } else if (searchMode === 'online') {
        const res = await api.searchOnlineResearch(targetQuery, limit)
        setOnlineResults(res.results || [])
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed to complete.')
    } finally {
      setLoading(false)
    }
  }

  const handleImportDocument = async (nasaId: string | number) => {
    if (DEMO_WRITES_DISABLED) {
      setImportNotice({
        id: String(nasaId),
        success: false,
        message: 'NASA document import is disabled for the local judge demo.',
      })
      return
    }

    const idStr = String(nasaId).trim()
    if (!idStr) return

    try {
      setImportingNasaId(idStr)
      setImportNotice(null)
      const res = await api.importNasaDocument(idStr)
      setImportNotice({
        id: idStr,
        success: true,
        message: `Successfully ingested document ${idStr}: ${res.passage_count ?? res.imported_passages_count ?? 0} passages extracted into supplemental store under status "${res.manual_review_status || res.status}".`,
      })
    } catch (err) {
      setImportNotice({
        id: idStr,
        success: false,
        message: err instanceof Error ? err.message : `Failed to import document ${idStr}`,
      })
    } finally {
      setImportingNasaId(null)
    }
  }

  const openReviewForTarget = (id: string, nasaId?: string, type = 'paper') => {
    setReviewTarget({ id, nasaId, type })
    setIsReviewModalOpen(true)
  }

  useEffect(() => {
    void executeSearch()
  }, [searchMode, limit])

  return (
    <div className="page-enter">
      {/* 1. Page Header with genuine NASA photography */}
      <PageMediaHeader
        image="/media/images/iss-earth-horizon.jpg"
        alt="International Space Station and Earth's horizon at night"
        credit="NASA Image Library · s134e010062 (Official NASA Media)"
      >
        <SectionHeader
          dark
          eyebrow="NASA RESEARCH / RETRIEVAL ENGINE"
          title="Extractive Scientific Evidence Search"
          detail="Query extracted NASA document text, catalog metadata, and verified experimental findings with transparent provenance."
          action={
            <StatusBadge tone="orange">
              <FileSearch size={13} />
              <span>Lexical Overlap Engine</span>
            </StatusBadge>
          }
        />
      </PageMediaHeader>

      {/* 2. Scientific Disclosure Banner */}
      <div className="safeguard-banner">
        <ShieldAlert size={16} style={{ color: '#D96C32', flexShrink: 0 }} />
        <span>
          <strong>PROVENANCE SAFEGUARD:</strong> Lexical ranking scores represent keyword overlap only.
          Extracted PDF passages remain heuristic classifications and must not be interpreted as certified fire-safety limits.
        </span>
      </div>

      <div className="safeguard-banner" style={{ backgroundColor: 'rgba(217, 108, 50, 0.1)', borderColor: 'rgba(217, 108, 50, 0.3)', color: '#7E3615' }}>
        <ShieldAlert size={16} style={{ color: '#D96C32', flexShrink: 0 }} />
        <span>
          <strong>LOCAL JUDGE DEMO:</strong> Review creation, review revisions, and NASA document import are disabled.
          Existing research and review records remain read-only.
        </span>
      </div>

      {/* 3. Search Workspace Box */}
      <div className="search-workspace-box">
        <SearchInput
          value={query}
          onChange={setQuery}
          onSubmit={() => executeSearch()}
          placeholder="Search NASA research (e.g. 'PMMA flame spread', 'oxygen concentration microgravity')..."
          buttonText="Execute Search"
          isLoading={loading}
        />

        <div className="filter-bar">
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600, color: '#171715' }}>
            <SlidersHorizontal size={13} />
            <span>MODE:</span>
          </div>

          <select
            value={searchMode}
            onChange={(e) => setSearchMode(e.target.value as SearchMode)}
            aria-label="Search strategy mode"
          >
            <option value="brief">Extractive Evidence Brief (/research/search)</option>
            <option value="combined">Combined Federated Search (/research/combined-search)</option>
            <option value="reviewed">Human Reviewed Evidence (/research/evidence-search)</option>
            <option value="passages">Document Passages (/research/nasa-passage-search)</option>
            <option value="online">NASA Online Repository (/research/online-search)</option>
          </select>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginLeft: '8px' }}>
            <span>EVIDENCE MODALITY:</span>
            <select
              value={modalityFilter}
              onChange={(e) => setModalityFilter(e.target.value)}
              aria-label="Filter evidence modality"
            >
              <option value="all">All Modalities</option>
              <option value="experimental">Experimental Only</option>
              <option value="simulation">Simulation Only</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginLeft: '8px' }}>
            <span>LIMIT:</span>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              aria-label="Result limit"
            >
              <option value={5}>5 Results</option>
              <option value={8}>8 Results</option>
              <option value={15}>15 Results</option>
              <option value={20}>20 Results</option>
            </select>
          </div>

          <button
            type="button"
            onClick={() => openReviewForTarget('', undefined, 'paper')}
            className="btn btn-secondary btn-sm"
            style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '6px' }}
          >
            <FileCheck2 size={13} style={{ color: '#D96C32' }} />
            <span>Peer Review Ledger</span>
          </button>
        </div>
      </div>

      {importNotice && (
        <div
          style={{
            margin: '0 0 16px',
            padding: '12px 16px',
            backgroundColor: importNotice.success ? 'rgba(74, 144, 94, 0.15)' : 'rgba(217, 83, 79, 0.15)',
            border: `1px solid ${importNotice.success ? 'rgba(74, 144, 94, 0.3)' : 'rgba(217, 83, 79, 0.3)'}`,
            borderRadius: '4px',
            color: importNotice.success ? '#82D898' : '#FF8888',
            fontSize: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '12px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CheckCircle2 size={14} />
            <span>{importNotice.message}</span>
          </div>
          <button
            onClick={() => setImportNotice(null)}
            style={{ background: 'none', border: 'none', color: 'inherit', cursor: 'pointer', padding: '2px' }}
          >
            <X size={14} />
          </button>
        </div>
      )}

      {error && (
        <ErrorState
          title="Search Service Notice"
          message={error}
          onRetry={() => executeSearch()}
        />
      )}

      {loading && <LoadingState message="Querying AeroGuard research stores..." />}

      {/* 4. Results Layout */}
      {!loading && !error && (
        <div className="responsive-research-split">
          {/* Main Results Column */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {/* Mode: Brief */}
            {searchMode === 'brief' && briefResponse && (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', color: '#686861', fontFamily: 'monospace' }}>
                  <span>
                    Returned <b>{briefResponse.results.length}</b> passages from <b>{briefResponse.summary?.source_document_count || 0}</b> distinct NASA source(s)
                  </span>
                  <span>Engine: {briefResponse.engine_version}</span>
                </div>

                {briefResponse.results.length === 0 ? (
                  <EmptyState
                    title="No matching passages found"
                    message="Try broader scientific terms such as 'combustion', 'oxygen', or 'PMMA'."
                  />
                ) : (
                  briefResponse.results
                    .filter((item) => {
                      if (modalityFilter === 'all') return true
                      return (item.evidence_modality || '').toLowerCase().includes(modalityFilter)
                    })
                    .map((item) => (
                      <div
                        key={`${item.record_id || item.source_id}-${item.nasa_id || 'unknown'}`}
                        className="research-card"
                        onClick={() =>
                          setSelectedItem({
                            id: item.record_id,
                            title: item.source_title,
                            nasaId: item.nasa_id || item.source_id,
                            excerpt: item.exact_source_excerpt,
                            sourceUrl: item.citation_url || item.source_url,
                            pdfPage: item.pdf_page_number,
                            evidenceType: item.evidence_role || item.evidence_modality,
                            verification: item.classification_review_status,
                            matchedTerms: item.matched_query_terms,
                            score: item.query_match_score,
                          })
                        }
                        style={{ cursor: 'pointer' }}
                      >
                        <div className="research-card-top">
                          <span className="nasa-id-pill">NASA ID: {item.nasa_id || item.source_id}</span>
                          <span className="relevance-score-badge">
                            Lexical score: {(item.query_match_score * 100).toFixed(0)}%
                          </span>
                        </div>

                        <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 600, color: '#171715', lineHeight: 1.4 }}>
                          {item.source_title}
                        </h3>

                        <div className="excerpt-box">
                          &ldquo;{item.exact_source_excerpt}&rdquo;
                        </div>

                        <div className="provenance-row">
                          <EvidenceBadge value={item.evidence_modality || item.evidence_role} />
                          <VerificationBadge value={item.classification_review_status} />
                          {item.pdf_page_number && (
                            <span>Page: {item.pdf_page_number}</span>
                          )}
                          <span>Role: {item.evidence_role}</span>
                        </div>
                      </div>
                    ))
                )}
              </>
            )}

            {/* Mode: Combined Federated */}
            {searchMode === 'combined' && combinedResponse && (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', color: '#686861', fontFamily: 'monospace' }}>
                  <span>
                    Local passages: <b>{combinedResponse.counts?.local_passages_returned || 0}</b> | Online NTRS records: <b>{combinedResponse.counts?.online_metadata_records || 0}</b>
                  </span>
                  <StatusBadge tone={combinedResponse.fallback_triggered ? 'warning' : 'verified'}>
                    {combinedResponse.fallback_triggered ? 'NTRS Fallback Active' : 'Local Sufficient'}
                  </StatusBadge>
                </div>

                {combinedResponse.local_evidence_brief?.results?.map((item) => (
                  <div
                    key={item.record_id}
                    className="research-card"
                    onClick={() =>
                      setSelectedItem({
                        id: item.record_id,
                        title: item.source_title,
                        nasaId: item.nasa_id,
                        excerpt: item.exact_source_excerpt,
                        sourceUrl: item.citation_url,
                        pdfPage: item.pdf_page_number,
                        evidenceType: item.evidence_role,
                        verification: item.classification_review_status,
                      })
                    }
                    style={{ cursor: 'pointer' }}
                  >
                    <div className="research-card-top">
                      <span className="nasa-id-pill">LOCAL: {item.nasa_id}</span>
                      <EvidenceBadge value={item.evidence_modality} />
                    </div>
                    <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 600 }}>{item.source_title}</h3>
                    <div className="excerpt-box">&ldquo;{item.exact_source_excerpt}&rdquo;</div>
                  </div>
                ))}

                {combinedResponse.online_search?.results?.map((item, idx) => (
                  <div
                    key={`online-${idx}`}
                    className="research-card"
                    style={{ borderStyle: 'dashed' }}
                    onClick={() =>
                      setSelectedItem({
                        id: String(item.nasa_id),
                        title: item.title,
                        nasaId: String(item.nasa_id),
                        excerpt: item.abstract,
                        sourceUrl: item.source_url,
                        evidenceType: 'Abstract scope',
                        verification: 'Metadata only',
                      })
                    }
                  >
                    <div className="research-card-top">
                      <span className="nasa-id-pill" style={{ backgroundColor: '#FAF9F6' }}>
                        NTRS CATALOG: {item.nasa_id}
                      </span>
                      <StatusBadge tone="neutral">Bibliographic / Abstract</StatusBadge>
                    </div>
                    <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 600 }}>{item.title}</h3>
                    <p style={{ margin: 0, fontSize: '12px', color: '#686861', lineHeight: 1.5 }}>
                      {item.abstract}
                    </p>
                  </div>
                ))}
              </>
            )}

            {/* Mode: Reviewed */}
            {searchMode === 'reviewed' && (
              <>
                {reviewedResults.length === 0 ? (
                  <EmptyState
                    title="No reviewed evidence matched"
                    message="Reviewed findings require explicit scientific review records. Try querying 'microgravity' or 'combustion'."
                  />
                ) : (
                  reviewedResults.map((item) => (
                    <div key={item.evidence_id} className="research-card">
                      <div className="research-card-top">
                        <span className="nasa-id-pill">EVIDENCE ID: {item.evidence_id}</span>
                        <StatusBadge tone="verified">Human Reviewed</StatusBadge>
                      </div>
                      <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 600 }}>{item.title}</h3>
                      <div className="excerpt-box">&ldquo;{item.finding}&rdquo;</div>
                      <div className="provenance-row">
                        <span>NASA ID: {item.nasa_id}</span>
                        {item.pdf_page && <span>PDF Page: {item.pdf_page}</span>}
                        {item.citation_url && (
                          <a
                            href={item.citation_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: '#D96C32' }}
                          >
                            <span>Original Paper</span>
                            <ExternalLink size={12} />
                          </a>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </>
            )}

            {/* Mode: Passages */}
            {searchMode === 'passages' && (
              <>
                {passageResults.length === 0 ? (
                  <EmptyState title="No document passages found" message="Try searching for another technical phrase." />
                ) : (
                  passageResults.map((item) => (
                    <div key={item.passage_id} className="research-card">
                      <div className="research-card-top">
                        <span className="nasa-id-pill">PASSAGE: {item.passage_id}</span>
                        <span className="relevance-score-badge">Score: {(item.score * 100).toFixed(0)}%</span>
                      </div>
                      <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 600 }}>{item.title}</h3>
                      <div className="excerpt-box">&ldquo;{item.text}&rdquo;</div>
                      <div className="provenance-row">
                        <span>NASA ID: {item.nasa_id}</span>
                        {item.page_number && <span>Page: {item.page_number}</span>}
                        {item.classification && <span>Class: {item.classification}</span>}
                      </div>
                    </div>
                  ))
                )}
              </>
            )}

            {/* Mode: NASA Online Repository */}
            {searchMode === 'online' && (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px', color: '#686861', fontFamily: 'monospace' }}>
                  <span>
                    Returned <b>{onlineResults.length}</b> online records from NASA Technical Reports Server (NTRS)
                  </span>
                  <StatusBadge tone="orange">Live NTRS API</StatusBadge>
                </div>

                {onlineResults.length === 0 ? (
                  <EmptyState
                    title="No online NASA documents found"
                    message="Query the live NASA NTRS repository with spaceflight terms like 'microgravity combustion' or 'flame spread'."
                  />
                ) : (
                  onlineResults.map((item) => (
                    <div key={String(item.nasa_id) || item.title} className="research-card">
                      <div className="research-card-top">
                        <span className="nasa-id-pill">NASA ID: {item.nasa_id}</span>
                        <span style={{ fontSize: '11px', color: '#B98555' }}>
                          {item.publication_date ? new Date(item.publication_date).getFullYear() : 'NTRS Archive'}
                        </span>
                      </div>

                      <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 600, color: '#171715', lineHeight: 1.4 }}>
                        {item.title}
                      </h3>

                      {item.authors && item.authors.length > 0 && (
                        <div style={{ fontSize: '11.5px', color: '#686861' }}>
                          Authors: {item.authors.map((a) => a.name).join(', ')}
                        </div>
                      )}

                      <div className="excerpt-box" style={{ maxHeight: '110px', overflowY: 'auto' }}>
                        {item.abstract || 'No abstract text returned from NTRS catalog.'}
                      </div>

                      <div className="provenance-row" style={{ flexWrap: 'wrap', gap: '8px' }}>
                        {item.subject_categories?.slice(0, 2).map((cat, cIdx) => (
                          <span key={cIdx} style={{ fontSize: '10.5px', color: '#858D77' }}>{cat}</span>
                        ))}

                        <div style={{ marginLeft: 'auto', display: 'flex', gap: '8px' }}>
                          <button
                            type="button"
                            onClick={() => handleImportDocument(item.nasa_id)}
                            disabled={DEMO_WRITES_DISABLED || importingNasaId === String(item.nasa_id)}
                            className="btn btn-primary btn-sm"
                            style={{ padding: '4px 10px', fontSize: '11px' }}
                            title="NASA document import is disabled for the local judge demo"
                          >
                            <Download size={12} className={importingNasaId === String(item.nasa_id) ? 'spin' : ''} />
                            <span>
                              {DEMO_WRITES_DISABLED ? 'Import Disabled' : importingNasaId === String(item.nasa_id) ? 'Ingesting PDF...' : 'Import to Store'}
                            </span>
                          </button>

                          <button
                            type="button"
                            onClick={() => openReviewForTarget(String(item.nasa_id), String(item.nasa_id), 'paper')}
                            disabled={DEMO_WRITES_DISABLED}
                            className="btn btn-secondary btn-sm"
                            style={{ padding: '4px 10px', fontSize: '11px' }}
                            title="Review writes are disabled for the local judge demo"
                          >
                            <FileCheck2 size={12} />
                            <span>Review Disabled</span>
                          </button>

                          {item.source_url && (
                            <a
                              href={item.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="btn btn-secondary btn-sm"
                              style={{ padding: '4px 10px', fontSize: '11px' }}
                            >
                              <ExternalLink size={12} />
                              <span>NTRS</span>
                            </a>
                          )}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </>
            )}
          </div>

          {/* Right Protocol & Limitations Panel */}
          <div>
            <EditorialCard variant="dark" style={{ position: 'sticky', top: '24px' }}>
              <div className="eyebrow eyebrow-dark">SEARCH PROTOCOL</div>
              <h3 style={{ margin: '0 0 12px', fontSize: '17px', color: '#FFFFFF' }}>
                Extractive Verification
              </h3>
              <p style={{ fontSize: '12px', lineHeight: 1.6, color: '#A2A299', marginBottom: '20px' }}>
                Every result retains explicit document citations, page numbers, and evidence modality classifications.
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '20px' }}>
                <div style={{ borderLeft: '2px solid #D96C32', paddingLeft: '10px' }}>
                  <b style={{ display: 'block', fontSize: '11px', color: '#FAF9F6' }}>01 / Normalized Scoring</b>
                  <span style={{ fontSize: '11px', color: '#A2A299' }}>
                    Lexical term overlap with parsed scientific queries.
                  </span>
                </div>
                <div style={{ borderLeft: '2px solid #B98555', paddingLeft: '10px' }}>
                  <b style={{ display: 'block', fontSize: '11px', color: '#FAF9F6' }}>02 / Scope Separation</b>
                  <span style={{ fontSize: '11px', color: '#A2A299' }}>
                    Experimental observations are strictly isolated from simulations and abstracts.
                  </span>
                </div>
                <div style={{ borderLeft: '2px solid #858D77', paddingLeft: '10px' }}>
                  <b style={{ display: 'block', fontSize: '11px', color: '#FAF9F6' }}>03 / Diversification</b>
                  <span style={{ fontSize: '11px', color: '#A2A299' }}>
                    Prioritizes distinct source documents over repetitive passage excerpts.
                  </span>
                </div>
              </div>

              <div style={{ padding: '12px', backgroundColor: 'rgba(217, 108, 50, 0.12)', border: '1px solid rgba(217, 108, 50, 0.28)', borderRadius: '4px' }}>
                <strong style={{ display: 'block', fontSize: '11px', color: '#D96C32', marginBottom: '4px' }}>
                  Scientific Safeguard
                </strong>
                <span style={{ fontSize: '10.5px', color: '#D3D3CB', lineHeight: 1.4, display: 'block' }}>
                  Passages retrieved do not represent independently certified fire safety claims. Always verify against primary paper PDFs.
                </span>
              </div>
            </EditorialCard>
          </div>
        </div>
      )}

      {/* 5. Detail Drawer */}
      {selectedItem && (
        <div className="drawer-scrim" onClick={() => setSelectedItem(null)}>
          <aside className="detail-drawer" onClick={(e) => e.stopPropagation()}>
            <button
              className="drawer-close"
              onClick={() => setSelectedItem(null)}
              aria-label="Close details"
            >
              <X size={20} />
            </button>

            <div className="eyebrow eyebrow-dark">RESEARCH PROVENANCE DETAIL</div>
            <span className="nasa-id-pill nasa-id-pill-dark" style={{ alignSelf: 'flex-start' }}>
              NASA ID: {selectedItem.nasaId}
            </span>

            <h2 style={{ margin: 0, fontSize: '19px', fontWeight: 700, color: '#FFFFFF', lineHeight: 1.35 }}>
              {selectedItem.title}
            </h2>

            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {selectedItem.evidenceType && <EvidenceBadge value={selectedItem.evidenceType} />}
              {selectedItem.verification && <VerificationBadge value={selectedItem.verification} />}
            </div>

            <div style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '16px' }}>
              <span style={{ display: 'block', fontSize: '10px', color: '#B98555', letterSpacing: '0.1em', marginBottom: '8px' }}>
                EXACT SOURCE EXCERPT
              </span>
              <div className="excerpt-box excerpt-box-dark">
                &ldquo;{selectedItem.excerpt}&rdquo;
              </div>
            </div>

            <div style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '16px' }}>
              <span style={{ display: 'block', fontSize: '10px', color: '#B98555', letterSpacing: '0.1em', marginBottom: '10px' }}>
                PROVENANCE METADATA
              </span>
              <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '8px', fontSize: '12px', color: '#D3D3CB' }}>
                <span style={{ color: '#A2A299' }}>Document ID:</span>
                <span style={{ fontFamily: 'monospace' }}>{selectedItem.id}</span>
                <span style={{ color: '#A2A299' }}>PDF Page:</span>
                <span>{selectedItem.pdfPage ? `Page ${selectedItem.pdfPage}` : 'Unpaginated'}</span>
                <span style={{ color: '#A2A299' }}>Classification:</span>
                <span>{selectedItem.evidenceType || 'Unclassified'}</span>
                <span style={{ color: '#A2A299' }}>Review Status:</span>
                <span>{selectedItem.verification || 'Not scientifically verified'}</span>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: 'auto', paddingTop: '16px' }}>
              <button
                type="button"
                onClick={() => openReviewForTarget(selectedItem.id, selectedItem.nasaId, 'paper')}
                disabled={DEMO_WRITES_DISABLED}
                className="btn btn-primary btn-full"
                title="Review writes are disabled for the local judge demo"
              >
                <FileCheck2 size={14} />
                <span>Review Writes Disabled</span>
              </button>

              {selectedItem.nasaId && (
                <button
                  type="button"
                  onClick={() => handleImportDocument(selectedItem.nasaId!)}
                  disabled={DEMO_WRITES_DISABLED || importingNasaId === String(selectedItem.nasaId)}
                  className="btn btn-secondary btn-full"
                  title="NASA document import is disabled for the local judge demo"
                >
                  <UploadCloud size={14} className={importingNasaId === String(selectedItem.nasaId) ? 'spin' : ''} />
                  <span>
                    {DEMO_WRITES_DISABLED
                      ? 'Import Disabled for Local Demo'
                      : importingNasaId === String(selectedItem.nasaId)
                      ? 'Ingesting PDF & Passages...'
                      : 'Import Document (POST /research/import)'}
                  </span>
                </button>
              )}

              {selectedItem.sourceUrl ? (
                <a
                  href={selectedItem.sourceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-secondary btn-full"
                >
                  <ExternalLink size={15} />
                  <span>Open Original NASA Citation</span>
                </a>
              ) : (
                <div style={{ fontSize: '11px', color: '#A2A299', textAlign: 'center' }}>
                  Local passage extraction · No external URL specified
                </div>
              )}
            </div>
          </aside>
        </div>
      )}

      {/* 6. Scientific Peer Review Ledger Modal */}
      <ReviewModal
        isOpen={isReviewModalOpen}
        onClose={() => setIsReviewModalOpen(false)}
        initialTargetId={reviewTarget.id}
        initialTargetType={reviewTarget.type}
        initialNasaId={reviewTarget.nasaId}
      />
    </div>
  )
}
