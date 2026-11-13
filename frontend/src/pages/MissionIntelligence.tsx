import { useEffect, useState } from 'react'
import {
  AlertTriangle,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Compass,
  Database,
  ExternalLink,
  FileCheck2,
  FileQuestion,
  Film,
  FlaskConical,
  HelpCircle,
  ImageIcon,
  Layers,
  MapPin,
  Moon,
  Play,
  Search,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
} from 'lucide-react'
import { api } from '../api/client'
import type { MissionIntelligenceResponse } from '../types/api'
import { PageMediaHeader } from '../components/ui/PageMediaHeader'
import { SectionHeader } from '../components/ui/SectionHeader'
import { StatCard } from '../components/ui/StatCard'
import { StatusBadge, EvidenceBadge, VerificationBadge } from '../components/ui/StatusBadge'
import { EditorialCard } from '../components/ui/GlassCard'
import { ErrorState, LoadingState } from '../components/ui/FeedbackStates'
import { ReviewModal } from '../components/ui/ReviewModal'

type MissionType = 'spacecraft' | 'moon' | 'mars'

interface MissionMediaConfig {
  image: string
  video: string
  poster: string
  alt: string
  credit: string
  eyebrow: string
  badgeLabel: string
  videoTitle: string
  gravityText: string
  icon: typeof Compass
}

const MISSION_CONFIG: Record<MissionType, MissionMediaConfig> = {
  spacecraft: {
    image: '/media/images/iss-earth-observation.jpg',
    video: '/media/videos/earth-views-iss-medium.mp4',
    poster: '/media/posters/earth-views-iss.jpg',
    alt: 'Earth observation from the International Space Station',
    credit: 'NASA · iss040e033340 (Spacecraft Habitat Observation)',
    eyebrow: 'MISSION SCENARIO: SPACECRAFT INTERNAL HABITAT (μG)',
    badgeLabel: 'ISS Microgravity (0g)',
    videoTitle: 'ISS Orbital Observation (NASA HDEV 720p)',
    gravityText: 'Near-zero gravity (μg · 10⁻⁴ to 10⁻⁶ g)',
    icon: Compass,
  },
  moon: {
    image: '/media/images/apollo-11-moon-surface.jpg',
    video: '/media/videos/moon-orion-flyby.mp4',
    poster: '/media/posters/moon-orion.jpg',
    alt: 'Buzz Aldrin on the lunar surface during Apollo 11',
    credit: 'NASA · as11-40-5903 (Apollo 11 lunar surface photograph)',
    eyebrow: 'MISSION SCENARIO: LUNAR SURFACE HABITAT (1/6G)',
    badgeLabel: 'Lunar Surface (1/6g)',
    videoTitle: 'Artemis I Orion Lunar Flyby Video (NASA JSC)',
    gravityText: 'Partial gravity (1.62 m/s² · 0.166 g)',
    icon: Moon,
  },
  mars: {
    image: '/media/images/perseverance-mars-surface.jpg',
    video: '/media/videos/mars-odyssey-orbit.mp4',
    poster: '/media/posters/mars-odyssey.jpg',
    alt: 'Perseverance rover on the surface of Mars',
    credit: 'NASA · PIA23764 (Perseverance Mars surface photograph)',
    eyebrow: 'MISSION SCENARIO: MARTIAN SURFACE HABITAT (3/8G)',
    badgeLabel: 'Martian Surface (3/8g)',
    videoTitle: 'Mars Odyssey Atmospheric Horizon Video (NASA JPL)',
    gravityText: 'Partial gravity (3.71 m/s² · 0.379 g)',
    icon: Sparkles,
  },
}

export default function MissionIntelligence() {
  const [mission, setMission] = useState<MissionType>('spacecraft')
  const [query, setQuery] = useState('oxygen concentration flame spread PMMA')
  const [fuel, setFuel] = useState('PMMA')
  const [oxygen, setOxygen] = useState('21')
  const [gravity, setGravity] = useState('microgravity')
  const [flow, setFlow] = useState('2 cm/s')

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [intelligenceData, setIntelligenceData] = useState<MissionIntelligenceResponse | null>(null)
  const [showVideoPlayer, setShowVideoPlayer] = useState(false)
  const [isReviewModalOpen, setIsReviewModalOpen] = useState(false)
  const [reviewTarget, setReviewTarget] = useState<{ id: string; type: string }>({
    id: 'spacecraft-mission-brief',
    type: 'mission_brief',
  })

  const media = MISSION_CONFIG[mission]

  const generateMissionBrief = async () => {
    if (!query || query.trim().length < 2) return
    setLoading(true)
    setError(null)
    try {
      const res = await api.getMissionIntelligence({
        query: query.trim(),
        mission_context: {
          mission,
          fuel,
          oxygen_concentration: oxygen,
          gravity_condition: gravity,
          flow_condition: flow,
        },
        limit: 8,
      })
      setIntelligenceData(res)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate mission intelligence orchestration.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void generateMissionBrief()
  }, [])

  return (
    <div className="page-enter">
      {/* 1. Page Header dynamically adapts with genuine NASA Moon, Mars, or Spacecraft photography */}
      <PageMediaHeader
        key={media.image}
        image={media.image}
        alt={media.alt}
        credit={media.credit}
      >
        <SectionHeader
          dark
          eyebrow={media.eyebrow}
          title="Mission Scenario Research Briefing"
          detail="Contextualizes microgravity combustion evidence against specific mission environments: Lunar, Martian, and Spacecraft habitats."
          action={
            <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
              <StatusBadge tone="orange">
                <media.icon size={13} />
                <span>{media.badgeLabel}</span>
              </StatusBadge>
              <button
                type="button"
                onClick={() => setShowVideoPlayer(!showVideoPlayer)}
                className="btn btn-sm btn-secondary"
                style={{ padding: '4px 10px', fontSize: '11px', display: 'inline-flex', alignItems: 'center', gap: '5px' }}
                title="Toggle Real NASA Mission Video"
              >
                {showVideoPlayer ? <ImageIcon size={13} /> : <Film size={13} />}
                <span>{showVideoPlayer ? 'Show Photo' : 'Watch NASA Video'}</span>
              </button>
            </div>
          }
        />
      </PageMediaHeader>

      {/* Optional NASA Mission Video Banner */}
      {showVideoPlayer && (
        <div
          className="dark-panel"
          style={{
            padding: '16px',
            marginBottom: '22px',
            border: '1px solid rgba(217, 108, 50, 0.4)',
            backgroundColor: '#101010',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Film size={15} style={{ color: '#D96C32' }} />
              <strong style={{ fontSize: '13px', color: '#FAF9F6' }}>
                {media.videoTitle}
              </strong>
            </div>
            <span style={{ fontSize: '11px', color: '#A2A299', fontFamily: 'monospace' }}>
              Official NASA Public Domain Footage
            </span>
          </div>

          <div style={{ position: 'relative', width: '100%', borderRadius: '4px', overflow: 'hidden', maxHeight: '340px', backgroundColor: '#000' }}>
            <video
              key={media.video}
              controls
              autoPlay
              muted
              loop
              playsInline
              poster={media.poster}
              style={{ width: '100%', height: 'auto', display: 'block', maxHeight: '340px', objectFit: 'contain' }}
            >
              <source src={media.video} type="video/mp4" />
              Your browser does not support HTML5 video playback.
            </video>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px', fontSize: '10.5px', color: '#A2A299', fontFamily: 'monospace' }}>
            <span>{media.credit}</span>
            <span>NASA Mission Archive</span>
          </div>
        </div>
      )}

      {/* 2. Mandatory Aerospace Engineering Safeguard */}
      <div className="safeguard-banner" style={{ backgroundColor: 'rgba(166, 75, 62, 0.12)', borderColor: 'rgba(166, 75, 62, 0.35)', color: '#6C1E15' }}>
        <ShieldAlert size={18} style={{ color: '#A64B3E', flexShrink: 0 }} />
        <div>
          <strong>AEROSPACE SAFETY SAFEGUARD:</strong> AeroGuard AI is an evidence-grounded research synthesis tool.
          It is <strong>NOT</strong> an autonomous, certified, or operational spacecraft fire-safety authority.
          All mission briefs remain research support and must undergo rigorous formal engineering review before operational adoption.
        </div>
      </div>

      {/* 3. Mission Parameters & Context Formulation Form */}
      <div className="search-workspace-box">
        <SectionHeader
          eyebrow="MISSION PARAMETERS FORMULATION"
          title="Mission Context & Conditions"
          detail="Define the targeted spacecraft scenario and operational conditions"
        />

        <div className="responsive-mission-form-grid">
          <div>
            <label style={{ display: 'block', fontSize: '11px', fontFamily: 'monospace', color: '#686861', marginBottom: '6px' }}>
              MISSION ENVIRONMENT
            </label>
            <select
              value={mission}
              onChange={(e) => {
                const val = e.target.value as MissionType
                setMission(val)
                if (val === 'moon') setGravity('1/6g')
                else if (val === 'mars') setGravity('3/8g')
                else setGravity('microgravity')
              }}
              style={{ width: '100%', padding: '9px 12px', border: '1px solid var(--border-light)', borderRadius: '4px', fontSize: '13px' }}
            >
              <option value="spacecraft">Spacecraft Internal Habitat (μg)</option>
              <option value="moon">Lunar Surface Habitat (1/6g · Moon)</option>
              <option value="mars">Martian Surface Habitat (3/8g · Mars)</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontFamily: 'monospace', color: '#686861', marginBottom: '6px' }}>
              FUEL / MATERIAL
            </label>
            <input
              type="text"
              value={fuel}
              onChange={(e) => setFuel(e.target.value)}
              placeholder="e.g. PMMA, Nomex, Cotton"
              style={{ width: '100%', padding: '9px 12px', border: '1px solid var(--border-light)', borderRadius: '4px', fontSize: '13px' }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontFamily: 'monospace', color: '#686861', marginBottom: '6px' }}>
              O₂ CONCENTRATION (% vol)
            </label>
            <input
              type="text"
              value={oxygen}
              onChange={(e) => setOxygen(e.target.value)}
              placeholder="e.g. 21, 30"
              style={{ width: '100%', padding: '9px 12px', border: '1px solid var(--border-light)', borderRadius: '4px', fontSize: '13px' }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '11px', fontFamily: 'monospace', color: '#686861', marginBottom: '6px' }}>
              FORCED FLOW CONDITION
            </label>
            <input
              type="text"
              value={flow}
              onChange={(e) => setFlow(e.target.value)}
              placeholder="e.g. 2 cm/s, quiescent"
              style={{ width: '100%', padding: '9px 12px', border: '1px solid var(--border-light)', borderRadius: '4px', fontSize: '13px' }}
            />
          </div>
        </div>

        <div style={{ marginTop: '14px' }}>
          <label style={{ display: 'block', fontSize: '11px', fontFamily: 'monospace', color: '#686861', marginBottom: '6px' }}>
            RESEARCH INQUIRY
          </label>
          <div className="responsive-mission-search-row">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              style={{ flex: 1, padding: '9px 12px', border: '1px solid var(--border-light)', borderRadius: '4px', fontSize: '13px' }}
            />
            <button
              className="btn btn-primary"
              onClick={() => generateMissionBrief()}
              disabled={loading}
            >
              <span>{loading ? 'Synthesizing...' : 'Generate Brief'}</span>
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      </div>

      {error && (
        <ErrorState
          title="Mission Intelligence Notice"
          message={error}
          onRetry={() => generateMissionBrief()}
        />
      )}

      {loading && <LoadingState message="Orchestrating mission intelligence across stores, BASS-II, and review DB..." />}

      {/* 4. Real Stats Overview */}
      {intelligenceData && !loading && (
        <div className="stat-grid">
          <StatCard
            label="Mission Context"
            value={mission.toUpperCase()}
            detail={`${fuel} · ${oxygen}% O₂`}
            icon={media.icon}
            highlight
          />
          <StatCard
            label="Extracted Papers"
            value={intelligenceData.evidence?.paper_count || 0}
            detail="Relevant source documents"
            icon={BookOpen}
          />
          <StatCard
            label="BASS-II Flight Matches"
            value={intelligenceData.bass2_evidence?.total_matching_records || 0}
            detail="Contextual experiment runs"
            icon={Database}
          />
          <StatCard
            label="Persistent Reviews"
            value={intelligenceData.reviews?.records?.length || 0}
            detail={intelligenceData.reviews?.accepted_review_present ? 'Accepted review present' : 'No accepted reviews'}
            icon={ShieldCheck}
          />
        </div>
      )}

      {/* 5. Mission Brief & Synthesis Layout */}
      {intelligenceData && !loading && (
        <div className="responsive-two-column-split">
          {/* Left Column: Mission Research Brief & Extracted Evidence */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {/* Executive Synthesis Card */}
            <EditorialCard variant="dark">
              <div className="eyebrow eyebrow-dark">EXECUTIVE MISSION SYNTHESIS</div>
              <h3 style={{ margin: '0 0 14px', fontSize: '19px', color: '#FFFFFF' }}>
                Operational Evidence Brief
              </h3>

              <div style={{ padding: '16px', backgroundColor: 'rgba(217,108,50,0.12)', borderLeft: '3px solid #D96C32', borderRadius: '0 4px 4px 0', marginBottom: '18px' }}>
                <span style={{ fontSize: '13px', color: '#FAF9F6', fontWeight: 600, lineHeight: 1.5, display: 'block' }}>
                  {intelligenceData.conclusion}
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px', fontSize: '12px', color: '#D3D3CB' }}>
                <div style={{ padding: '12px', backgroundColor: '#22221F', borderRadius: '4px' }}>
                  <b style={{ display: 'block', color: '#FAF9F6', marginBottom: '4px' }}>Target Destination</b>
                  <span style={{ textTransform: 'capitalize' }}>{mission} Habitat ({media.gravityText})</span>
                </div>
                <div style={{ padding: '12px', backgroundColor: '#22221F', borderRadius: '4px' }}>
                  <b style={{ display: 'block', color: '#FAF9F6', marginBottom: '4px' }}>Target Material</b>
                  <span>{fuel} (reported conditions)</span>
                </div>
              </div>
            </EditorialCard>

            {/* BASS-II Contextual Flight Runs */}
            <EditorialCard variant="charcoal">
              <SectionHeader
                dark
                eyebrow="BASS-II FLIGHT DATA CONTEXT"
                title="Matching Experimental Test Runs"
                detail="Raw NASA PSI-25 table records filtered by material and query"
                action={
                  <StatusBadge tone="orange">
                    {intelligenceData.bass2_evidence?.total_matching_records || 0} Runs Found
                  </StatusBadge>
                }
              />

              {intelligenceData.bass2_evidence?.returned_records && intelligenceData.bass2_evidence.returned_records.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {intelligenceData.bass2_evidence.returned_records.slice(0, 5).map((item, idx) => (
                    <div key={idx} style={{ padding: '12px', backgroundColor: '#151515', borderRadius: '4px', border: '1px solid rgba(255,255,255,0.08)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                        <span className="nasa-id-pill nasa-id-pill-dark">
                          Test: {item.record?.PI}-{item.record?.['Test #']}
                        </span>
                        <span style={{ fontSize: '11px', color: '#A2A299', fontFamily: 'monospace' }}>
                          O₂: {item.record?.['Calibrated  initial O2 % by vol ']}% → {item.record?.['Calibrated final O2 % by vol']}%
                        </span>
                      </div>
                      <div style={{ fontSize: '12px', color: '#FAF9F6' }}>
                        {item.record?.['Fuel Sample Material']}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ padding: '16px', backgroundColor: '#151515', borderRadius: '4px', fontSize: '12px', color: '#A2A299' }}>
                  No exact BASS-II flight run directly matched the material string &ldquo;{fuel}&rdquo;.
                </div>
              )}

              <div style={{ marginTop: '12px', fontSize: '11px', color: '#A2A299' }}>
                Notice: BASS-II records provide condition and instrument metadata, not a verified flame spread rate.
              </div>
            </EditorialCard>

            {/* Document Evidence Section */}
            <EditorialCard variant="dark">
              <SectionHeader
                dark
                eyebrow="SUPPORTING DOCUMENT EVIDENCE"
                title="Retrieved NASA Source Passages"
                detail="Excerpts retrieved from primary stores matching the mission scenario"
              />

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '14px' }}>
                {intelligenceData.evidence?.papers?.map((paper, pIdx) => (
                  <div key={pIdx} style={{ padding: '14px', backgroundColor: '#181816', borderRadius: '4px', border: '1px solid rgba(255,255,255,0.08)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <span className="nasa-id-pill nasa-id-pill-dark">NASA ID: {paper.nasa_id || paper.document_id}</span>
                      <EvidenceBadge value={paper.evidence_classification} />
                    </div>
                    <h4 style={{ margin: '0 0 8px', fontSize: '14px', color: '#FFFFFF' }}>
                      {paper.source_title}
                    </h4>
                    {paper.claims && paper.claims.length > 0 && (
                      <div className="excerpt-box excerpt-box-dark" style={{ fontSize: '12px' }}>
                        &ldquo;{paper.claims[0].claim_text}&rdquo;
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </EditorialCard>
          </div>

          {/* Right Column: Mission Governance & Persistent Review Audit */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {/* Mission Governance & Review Status */}
            <EditorialCard variant="charcoal">
              <SectionHeader
                dark
                eyebrow="HUMAN REVIEW AUDIT TRAIL"
                title="Persistent Review Ledger"
                detail="Recorded reviews retrieved directly from SQLite review storage"
                action={
                  <VerificationBadge value={intelligenceData.reviews?.accepted_review_present ? 'Verified' : 'Review Required'} />
                }
              />

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                  <span style={{ fontSize: '12px', color: '#A2A299' }}>Total Review Records:</span>
                  <span style={{ fontSize: '12px', fontFamily: 'monospace', color: '#FAF9F6' }}>
                    {intelligenceData.reviews?.records?.length || 0}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', paddingBottom: '8px', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
                  <span style={{ fontSize: '12px', color: '#A2A299' }}>Accepted Reviews:</span>
                  <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#FAF9F6' }}>
                    {intelligenceData.reviews?.accepted_review_present ? 'Present' : 'None Present'}
                  </span>
                </div>
              </div>

              <div style={{ marginTop: '14px', padding: '10px', backgroundColor: 'rgba(0,0,0,0.3)', borderRadius: '4px', fontSize: '10.5px', color: '#A2A299', lineHeight: 1.4 }}>
                Review decisions are persisted in the SQLite ledger, but reviewer identity is unauthenticated. Accepted reviews do not constitute NASA certification.
              </div>

              <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
                <button
                  type="button"
                  onClick={() => {
                    setReviewTarget({ id: `${mission}-mission-brief`, type: 'mission_brief' })
                    setIsReviewModalOpen(true)
                  }}
                  className="btn btn-secondary btn-full btn-sm"
                  style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}
                >
                  <FileCheck2 size={13} style={{ color: '#D96C32' }} />
                  <span>Inspect Review Ledger</span>
                </button>
              </div>
            </EditorialCard>

            {/* Critical Research Gaps */}
            <EditorialCard variant="dark">
              <div className="eyebrow eyebrow-dark">CRITICAL EVIDENCE GAPS</div>
              <h3 style={{ margin: '0 0 12px', fontSize: '16px', color: '#FFFFFF' }}>
                Unresolved Flight Conditions
              </h3>
              {intelligenceData.research_gaps && intelligenceData.research_gaps.length > 0 ? (
                <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '12px', color: '#D3D3CB', display: 'flex', flexDirection: 'column', gap: '8px', lineHeight: 1.4 }}>
                  {intelligenceData.research_gaps.map((gap, gIdx) => (
                    <li key={gIdx}>{gap.description}</li>
                  ))}
                </ul>
              ) : (
                <div style={{ fontSize: '12px', color: '#A2A299' }}>
                  Atmospheric flow and gravity level comparability must be qualified by flight testing.
                </div>
              )}
            </EditorialCard>

            {/* Suggested Follow-up Inquiries */}
            <EditorialCard variant="charcoal">
              <div className="eyebrow eyebrow-dark">RECOMMENDED INQUIRIES</div>
              <h3 style={{ margin: '0 0 12px', fontSize: '16px', color: '#FFFFFF' }}>
                Suggested Research Questions
              </h3>
              {intelligenceData.suggested_research_questions && intelligenceData.suggested_research_questions.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {intelligenceData.suggested_research_questions.map((q) => (
                    <div key={`${q.question}-${q.gap_ids.join(',')}`} style={{ padding: '8px 10px', backgroundColor: 'rgba(0,0,0,0.3)', borderRadius: '4px', fontSize: '11.5px', color: '#FAF9F6', display: 'flex', gap: '6px', alignItems: 'flex-start' }}>
                      <ArrowRight size={13} style={{ color: '#D96C32', flexShrink: 0, marginTop: '2px' }} />
                      <span>{q.question}</span>
                      {q.supporting_source_ids.length > 0 && (
                        <small style={{ color: '#A2A299' }}>Sources: {q.supporting_source_ids.join(', ')}</small>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ fontSize: '12px', color: '#A2A299' }}>
                  Which studies test {fuel} at {oxygen}% O₂ under forced microgravity flow?
                </div>
              )}
            </EditorialCard>
          </div>
        </div>
      )}

      {/* Peer Review Ledger Modal */}
      <ReviewModal
        isOpen={isReviewModalOpen}
        onClose={() => setIsReviewModalOpen(false)}
        initialTargetId={reviewTarget.id}
        initialTargetType={reviewTarget.type}
      />
    </div>
  )
}
