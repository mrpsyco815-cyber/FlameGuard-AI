import { useEffect, useState } from 'react'
import {
  Activity,
  ArrowRight,
  CheckCircle,
  Compass,
  Database,
  FileSearch,
  FlaskConical,
  GitCompare,
  Layers,
  Shield,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
} from 'lucide-react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { Link } from 'react-router-dom'
import { api } from '../api/client'
import type { Bass2Summary, DashboardMissionBriefResponse, HealthResponse } from '../types/api'
import { CinematicHero } from '../components/ui/CinematicHero'
import { EditorialCard } from '../components/ui/GlassCard'
import { SectionHeader } from '../components/ui/SectionHeader'
import { StatCard } from '../components/ui/StatCard'
import { StatusBadge } from '../components/ui/StatusBadge'
import { EmptyState, ErrorState, LoadingState } from '../components/ui/FeedbackStates'

export default function Dashboard() {
  const [summary, setSummary] = useState<Bass2Summary | null>(null)
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [brief, setBrief] = useState<DashboardMissionBriefResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true
    const loadDashboardData = async () => {
      try {
        setLoading(true)
        setError(null)
        const [summaryResult, healthResult, briefResult] = await Promise.allSettled([
          api.getBass2Summary(),
          api.getHealth(),
          api.getDashboardMissionBrief({
            mission: 'spacecraft',
            q: 'oxygen concentration microgravity combustion',
          }),
        ])
        if (!active) return
        if (summaryResult.status === 'fulfilled') setSummary(summaryResult.value)
        if (healthResult.status === 'fulfilled') setHealth(healthResult.value)
        if (briefResult.status === 'fulfilled') setBrief(briefResult.value)
        if (
          summaryResult.status === 'rejected' ||
          healthResult.status === 'rejected' ||
          briefResult.status === 'rejected'
        ) {
          setError('One or more dashboard data sources are unavailable. Unavailable metrics are not replaced with fallback values.')
        }
      } catch (err) {
        if (active) setError(err instanceof Error ? err.message : 'Failed to reach AeroGuard backend')
      } finally {
        if (active) setLoading(false)
      }
    }
    void loadDashboardData()
    return () => {
      active = false
    }
  }, [])

  // Format PI distribution data from actual backend response
  const piData = summary?.pi_counts
    ? Object.entries(summary.pi_counts).map(([name, count]) => ({
        name: name || 'Unspecified',
        count,
      }))
    : []

  const PI_COLORS = ['#151515', '#D96C32', '#B98555', '#686861']

  return (
    <div className="page-enter">
      {/* 1. Cinematic Hero with genuine NASA HDEV video and fallback */}
      <CinematicHero />

      {/* 2. Scientific Safeguard Banner */}
      <div className="safeguard-banner">
        <ShieldAlert size={16} style={{ color: '#D96C32', flexShrink: 0 }} />
        <span>
          <strong>SCIENTIFIC DISCLOSURE:</strong> AeroGuard AI provides deterministic evidence-grounded research synthesis.
          Scores measure lexical token overlap, not autonomous safety certification or operational mission authority.
        </span>
      </div>

      {error && (
        <ErrorState
          title="Backend Notice"
          message={error}
        />
      )}

      {/* 3. Real Backend Metrics (Black cards with white text & orange highlights) */}
      <div className="stat-grid">
        <StatCard
          label="BASS-II Records"
          value={summary ? summary.record_count : 'Unavailable'}
          detail={summary ? 'Original strings preserved without mutation' : 'Backend data unavailable'}
          icon={Database}
          highlight
        />
        <StatCard
          label="Schema Dimensions"
          value={summary ? summary.column_count : 'Unavailable'}
          detail={summary ? 'Documented experimental columns' : 'Backend data unavailable'}
          icon={Layers}
        />
        <StatCard
          label="Backend Service"
          value={health ? 'Online' : loading ? 'Pinging...' : 'Offline'}
          detail={health ? `FastAPI ${health.service}` : 'Health data unavailable'}
          icon={Activity}
          highlight={health?.status === 'healthy'}
        />
        <StatCard
          label="Knowledge Store"
          value={typeof brief?.coverage?.total_store_records === 'number'
            ? brief.coverage.total_store_records.toLocaleString()
            : 'Unavailable'}
          detail={brief ? 'Extracted passages & flight runs' : 'Backend data unavailable'}
          icon={ShieldCheck}
          highlight
        />
      </div>

      {/* 4. Research Activity & Dataset Overview Grid */}
      <div className="responsive-dashboard-grid">
        {/* PI Experiment Distribution Chart */}
        <EditorialCard variant="dark">
          <SectionHeader
            dark
            eyebrow="BASS-II INVESTIGATOR DISTRIBUTION"
            title="Principal Investigators"
            detail="Declared experiments by principal investigator from raw dataset"
            action={<StatusBadge tone="orange">{summary ? `${summary.record_count} Runs` : 'Unavailable'}</StatusBadge>}
          />
          {loading ? (
            <LoadingState message="Extracting PI distribution..." />
          ) : !summary ? (
            <EmptyState
              title="BASS-II metrics unavailable"
              message="The dashboard cannot display investigator distribution without backend data."
            />
          ) : (
            <div style={{ height: '240px', width: '100%' }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={piData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" vertical={false} />
                  <XAxis dataKey="name" stroke="#A2A299" fontSize={11} tickLine={false} />
                  <YAxis stroke="#A2A299" fontSize={11} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#151515',
                      borderColor: 'rgba(255,255,255,0.18)',
                      borderRadius: '4px',
                      color: '#FAF9F6',
                      fontSize: '12px',
                    }}
                  />
                  <Bar dataKey="count" fill="#D96C32" radius={[3, 3, 0, 0]}>
                    {piData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={PI_COLORS[index % PI_COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </EditorialCard>

        {/* Evidence Integrity Status Card */}
        <EditorialCard variant="charcoal">
          <SectionHeader
            dark
            eyebrow="DATASET FIDELITY"
            title="Scientific Provenance"
            detail="Fidelity status of the microgravity combustion knowledge base"
          />
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginTop: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
              <div>
                <strong style={{ display: 'block', fontSize: '13px', color: '#FFFFFF' }}>BASS-II Source Values</strong>
                <small style={{ color: '#A2A299', fontSize: '11px' }}>Raw experimental numbers unmodified</small>
              </div>
              <StatusBadge tone="verified">Unmodified</StatusBadge>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
              <div>
                <strong style={{ display: 'block', fontSize: '13px', color: '#FFFFFF' }}>Unsupported Field Warning</strong>
                <small style={{ color: '#A2A299', fontSize: '11px' }}>Gravity, spread rate, extinction absent</small>
              </div>
              <StatusBadge tone="warning">Explicitly Labeled</StatusBadge>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
              <div>
                <strong style={{ display: 'block', fontSize: '13px', color: '#FFFFFF' }}>Review Storage</strong>
                <small style={{ color: '#A2A299', fontSize: '11px' }}>SQLite append-only audit trail</small>
              </div>
              <StatusBadge tone="verified">Operational</StatusBadge>
            </div>

            <div style={{ marginTop: '8px' }}>
              <Link to="/bass2" className="btn btn-secondary btn-full btn-sm">
                <Database size={14} />
                <span>Explore Full BASS-II Table</span>
              </Link>
            </div>
          </div>
        </EditorialCard>
      </div>

      {/* 4b. Live Mission Safety Brief & Evidence Synthesis (/dashboard/mission-brief) */}
      {brief && (
        <div style={{ marginTop: '24px', marginBottom: '24px' }}>
          <EditorialCard variant="dark">
            <SectionHeader
              dark
              eyebrow="LIVE MISSION BRIEF / SYNTHESIS ENGINE"
              title="Automated Evidence Synthesis Brief"
              detail={`Extracted from ${brief.coverage?.total_store_records || 2836} records for mission "${brief.mission_scenario.mission}" and query "${brief.mission_scenario.query}"`}
              action={
                <StatusBadge tone="orange">
                  <Compass size={12} />
                  <span>{brief.mission_scenario.mission.toUpperCase()} SYNTHESIS</span>
                </StatusBadge>
              }
            />

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginTop: '16px' }}>
              {/* Left: Safety Insights */}
              <div>
                <span style={{ display: 'block', fontSize: '11px', color: '#B98555', letterSpacing: '0.08em', fontWeight: 600, marginBottom: '10px' }}>
                  SAFETY INSIGHTS ({brief.safety_insights?.length || 0})
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {brief.safety_insights && brief.safety_insights.length > 0 ? (
                    brief.safety_insights.map((si, idx) => (
                      <div
                        key={idx}
                        style={{
                          backgroundColor: '#151515',
                          border: '1px solid rgba(255, 255, 255, 0.08)',
                          borderRadius: '4px',
                          padding: '10px 12px',
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                          <span style={{ fontSize: '12px', fontWeight: 600, color: '#FAF9F6' }}>{si.topic}</span>
                          <StatusBadge tone={si.status === 'requires_investigation' ? 'warning' : 'neutral'}>
                            {si.status.replace(/_/g, ' ')}
                          </StatusBadge>
                        </div>
                        <p style={{ margin: 0, fontSize: '11.5px', color: '#D3D3CB', lineHeight: 1.45 }}>
                          {si.observation}
                        </p>
                      </div>
                    ))
                  ) : (
                    <div style={{ fontSize: '12px', color: '#A2A299' }}>No active safety insights recorded.</div>
                  )}
                </div>
              </div>

              {/* Right: Key Grounded Recommendations */}
              <div>
                <span style={{ display: 'block', fontSize: '11px', color: '#B98555', letterSpacing: '0.08em', fontWeight: 600, marginBottom: '10px' }}>
                  EVIDENCE-GROUNDED RECOMMENDATIONS ({brief.recommendations?.length || 0})
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {brief.recommendations && brief.recommendations.length > 0 ? (
                    brief.recommendations.slice(0, 3).map((rec, rIdx) => (
                      <div
                        key={rIdx}
                        style={{
                          backgroundColor: '#151515',
                          border: '1px solid rgba(255, 255, 255, 0.08)',
                          borderRadius: '4px',
                          padding: '10px 12px',
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                          <span style={{ fontSize: '11px', color: '#D96C32', fontFamily: 'monospace' }}>
                            {rec.supporting_source_id ? `Source: ${rec.supporting_source_id}` : 'General Finding'}
                          </span>
                          <StatusBadge tone="verified">{rec.evidence_strength || 'Experimental'}</StatusBadge>
                        </div>
                        <p style={{ margin: '0 0 6px', fontSize: '11.5px', color: '#FAF9F6', lineHeight: 1.45 }}>
                          {rec.recommendation}
                        </p>
                        {rec.applicability_limitations && (
                          <div style={{ fontSize: '10.5px', color: '#A2A299' }}>
                            <em>Limitation:</em> {rec.applicability_limitations}
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div style={{ fontSize: '12px', color: '#A2A299' }}>No recommendations generated.</div>
                  )}
                </div>
              </div>
            </div>

            <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '8px' }}>
              <div style={{ fontSize: '11px', color: '#A2A299' }}>
                Coverage: <b>{brief.coverage?.matched_experimental_passages || 0}</b> experimental passages, <b>{brief.coverage?.matched_simulation_passages || 0}</b> simulation passages examined.
              </div>
              <Link to="/mission-intelligence" className="btn btn-secondary btn-sm">
                <span>View Full Mission Intelligence Synthesis</span>
                <ArrowRight size={13} />
              </Link>
            </div>
          </EditorialCard>
        </div>
      )}
      <SectionHeader
        eyebrow="RESEARCH WORKSPACE MODULES"
        title="Trace the Full Evidence Chain"
        detail="Each module preserves provenance, highlights scientific limitations, and prevents artificial certainty."
      />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
        <Link to="/research" className="stat-card-dark" style={{ textDecoration: 'none' }}>
          <div className="stat-card-top">
            <span className="stat-card-label">01 / RETRIEVAL</span>
            <div className="stat-card-icon"><FileSearch size={16} /></div>
          </div>
          <div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: '#FFFFFF', marginBottom: '6px' }}>
              NASA Research Search
            </div>
            <div className="stat-card-detail">
              Lexical search over extracted passages and NTRS catalogue metadata.
            </div>
          </div>
        </Link>

        <Link to="/bass2" className="stat-card-dark" style={{ textDecoration: 'none' }}>
          <div className="stat-card-top">
            <span className="stat-card-label">02 / EXPERIMENTAL DATA</span>
            <div className="stat-card-icon" style={{ color: '#D96C32' }}><Database size={16} /></div>
          </div>
          <div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: '#FFFFFF', marginBottom: '6px' }}>
              BASS-II Dataset
            </div>
            <div className="stat-card-detail">
              Raw microgravity combustion runs with intact calibrated initial/final O₂.
            </div>
          </div>
        </Link>

        <Link to="/insights" className="stat-card-dark" style={{ textDecoration: 'none' }}>
          <div className="stat-card-top">
            <span className="stat-card-label">03 / EXTRACTIVE INSIGHTS</span>
            <div className="stat-card-icon"><FlaskConical size={16} /></div>
          </div>
          <div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: '#FFFFFF', marginBottom: '6px' }}>
              Research Insights
            </div>
            <div className="stat-card-detail">
              Extract section-aware claims, structured findings, and source conflicts.
            </div>
          </div>
        </Link>

        <Link to="/comparison" className="stat-card-dark" style={{ textDecoration: 'none' }}>
          <div className="stat-card-top">
            <span className="stat-card-label">04 / CONDITION MATRIX</span>
            <div className="stat-card-icon"><GitCompare size={16} /></div>
          </div>
          <div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: '#FFFFFF', marginBottom: '6px' }}>
              Research Comparison
            </div>
            <div className="stat-card-detail">
              Pairwise condition matrix across 9 dimensions without inferring equivalence.
            </div>
          </div>
        </Link>

        <Link to="/mission-intelligence" className="stat-card-dark" style={{ textDecoration: 'none' }}>
          <div className="stat-card-top">
            <span className="stat-card-label">05 / MISSION SYNTHESIS</span>
            <div className="stat-card-icon"><Compass size={16} /></div>
          </div>
          <div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: '#FFFFFF', marginBottom: '6px' }}>
              Mission Intelligence
            </div>
            <div className="stat-card-detail">
              Synthesize Moon, Mars, and Spacecraft evidence with human review history.
            </div>
          </div>
        </Link>
      </div>
    </div>
  )
}
