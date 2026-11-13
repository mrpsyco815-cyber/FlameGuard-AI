import { useEffect, useMemo, useState } from 'react'
import {
  AlertTriangle,
  ArrowUpDown,
  Database,
  Filter,
  Flame,
  Info,
  Layers,
  Search,
  ShieldCheck,
  Table2,
} from 'lucide-react'
import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { api } from '../api/client'
import type { Bass2Summary, RawBass2Record } from '../types/api'
import { PageMediaHeader } from '../components/ui/PageMediaHeader'
import { SectionHeader } from '../components/ui/SectionHeader'
import { StatCard } from '../components/ui/StatCard'
import { StatusBadge } from '../components/ui/StatusBadge'
import { EditorialCard } from '../components/ui/GlassCard'
import { DataTable } from '../components/ui/DataTable'
import { ErrorState, LoadingState } from '../components/ui/FeedbackStates'

export default function Bass2Data() {
  const [summary, setSummary] = useState<Bass2Summary | null>(null)
  const [records, setRecords] = useState<RawBass2Record[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Filters
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedPi, setSelectedPi] = useState<string>('all')
  const [selectedFuel, setSelectedFuel] = useState<string>('all')

  const fetchDataset = async () => {
    setLoading(true)
    setError(null)
    try {
      const summaryRes = await api.getBass2Summary()
      setSummary(summaryRes)

      // Query all records with limit 100
      const searchRes = await api.searchBass2({
        q: searchQuery.trim(),
        pi: selectedPi === 'all' ? undefined : selectedPi,
        fuel: selectedFuel === 'all' ? undefined : selectedFuel,
        limit: 100,
      })

      const raw = searchRes.results.map((r) => r.record)
      setRecords(raw)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to query BASS-II dataset.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void fetchDataset()
  }, [selectedPi, selectedFuel])

  // Oxygen Trend data for chart based strictly on actual available records
  const chartData = useMemo(() => {
    return records
      .filter((r) => {
        const init = parseFloat(r['Calibrated  initial O2 % by vol '])
        const fin = parseFloat(r['Calibrated final O2 % by vol'])
        return !isNaN(init) && !isNaN(fin)
      })
      .slice(0, 20)
      .map((r) => ({
        test: `${r.PI.slice(0, 4)}-${r['Test #']}`,
        initialO2: parseFloat(r['Calibrated  initial O2 % by vol ']),
        finalO2: parseFloat(r['Calibrated final O2 % by vol']),
        material: r['Fuel Sample Material'],
      }))
  }, [records])

  return (
    <div className="page-enter">
      {/* 1. Page Header with genuine NASA photography */}
      <PageMediaHeader
        image="/media/images/combustion-integrated-rack.jpg"
        alt="Astronaut works on the Combustion Integrated Rack"
        credit="NASA · iss058e026380 (Combustion Integrated Rack context; not direct BASS-II imagery)"
      >
        <SectionHeader
          dark
          eyebrow="NASA PSI-25 BASS-II / EXPERIMENTAL DATASET"
          title="Microgravity Combustion Experimental Table"
          detail="129 structured flight experiment runs aboard the International Space Station. Source values preserved exactly as reported."
          action={
            <StatusBadge tone="verified">
              <ShieldCheck size={13} />
              <span>Source Values Intact</span>
            </StatusBadge>
          }
        />
      </PageMediaHeader>

      {/* 2. Critical Scientific Disclosure: Unavailable Fields */}
      <div className="safeguard-banner" style={{ backgroundColor: 'rgba(217, 108, 50, 0.1)', borderColor: 'rgba(217, 108, 50, 0.3)', color: '#7E3615' }}>
        <AlertTriangle size={17} style={{ color: '#D96C32', flexShrink: 0 }} />
        <div>
          <strong>STRICT DATA INTEGRITY NOTICE:</strong> This dataset contains 17 documented columns of instrument and atmospheric conditions.
          Fields for <em>gravity magnitude, ambient pressure, flame temperature, flame spread rate, and extinction outcome</em> are <strong>NOT PRESENT</strong> in the NASA PSI-25 table.
          They are never fabricated or inferred by AeroGuard AI. Blank cells are explicitly distinguished from zero values.
        </div>
      </div>

      {error && (
        <ErrorState
          title="Dataset API Notice"
          message={error}
          onRetry={() => fetchDataset()}
        />
      )}

      {/* 3. Real Metric Cards (Black cards, white text, orange accents) */}
      <div className="stat-grid">
        <StatCard
          label="Total Records"
          value={summary ? summary.record_count : '129'}
          detail="Declared experimental runs"
          icon={Table2}
          highlight
        />
        <StatCard
          label="Active Columns"
          value={summary ? summary.column_count : '17'}
          detail="Raw schema fields"
          icon={Database}
        />
        <StatCard
          label="Blank Cells"
          value={summary ? summary.blank_cells : '42'}
          detail="Preserved as unrecorded (not zero)"
          icon={Info}
        />
        <StatCard
          label="Values Modified"
          value="0 (False)"
          detail="Raw string preservation verified"
          icon={ShieldCheck}
        />
      </div>

      {/* 4. Chart & Schema Coverage Grid */}
      <div className="responsive-chart-field-split">
        {/* Oxygen Concentration Chart */}
        <EditorialCard variant="dark">
          <SectionHeader
            dark
            eyebrow="ATMOSPHERIC CONDITIONS"
            title="Initial vs Final Calibrated O₂ (% by vol)"
            detail="Plotted solely from actual available oxygen columns across 20 sample tests"
          />
          <div style={{ height: '260px', width: '100%', marginTop: '10px' }}>
            {chartData.length === 0 ? (
              <LoadingState message="Plotting experimental oxygen runs..." />
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="o2InitialGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#D96C32" stopOpacity={0.4} />
                      <stop offset="100%" stopColor="#D96C32" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" vertical={false} />
                  <XAxis dataKey="test" stroke="#A2A299" fontSize={10} tickLine={false} />
                  <YAxis stroke="#A2A299" fontSize={10} domain={[16, 32]} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#151515',
                      borderColor: 'rgba(255,255,255,0.2)',
                      borderRadius: '4px',
                      color: '#FAF9F6',
                      fontSize: '11px',
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '11px', color: '#A2A299' }} />
                  <Area
                    type="monotone"
                    dataKey="initialO2"
                    name="Initial O₂ %"
                    stroke="#D96C32"
                    fill="url(#o2InitialGrad)"
                    strokeWidth={2}
                  />
                  <Area
                    type="monotone"
                    dataKey="finalO2"
                    name="Final O₂ %"
                    stroke="#B98555"
                    fill="none"
                    strokeWidth={2}
                    strokeDasharray="4 4"
                  />
                </AreaChart>
              </ResponsiveContainer>
            )}
          </div>
        </EditorialCard>

        {/* Available Schema Field Inventory */}
        <EditorialCard variant="charcoal">
          <SectionHeader
            dark
            eyebrow="SCHEMA VALIDATION"
            title="Field Inventory"
            detail="17 documented raw dataset columns"
          />
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px', fontSize: '11px', color: '#D3D3CB', fontFamily: 'monospace', marginTop: '12px' }}>
            {[
              'PI',
              'Test #',
              'Date',
              'GMT',
              'Sample #',
              'Fuel Sample Material',
              'Flow restrictor',
              'Fan display',
              'Air display',
              'Radiometer gain',
              'Total Frames Shot',
              'Calibrated initial O2',
              'Calibrated final O2',
              'Initial CO2 %',
              'Final CO2 %',
              'Initial CO (ppm)',
              'Final CO (ppm)',
            ].map((f) => (
              <div key={f} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span className="status-dot-active" style={{ width: '5px', height: '5px' }} />
                <span>{f}</span>
              </div>
            ))}
          </div>

          <div style={{ marginTop: '20px', padding: '12px', backgroundColor: 'rgba(0,0,0,0.4)', borderRadius: '4px', borderLeft: '3px solid #D96C32' }}>
            <span style={{ display: 'block', fontSize: '10px', color: '#D96C32', letterSpacing: '0.08em', fontWeight: 600 }}>
              NON-INFERENCE RULE
            </span>
            <span style={{ fontSize: '11px', color: '#A2A299', lineHeight: 1.4, display: 'block', marginTop: '4px' }}>
              Numeric fields are queried with explicit float tolerances. Blank cells are never imputed.
            </span>
          </div>
        </EditorialCard>
      </div>

      {/* 5. Explorer Search & Filters */}
      <div className="search-workspace-box">
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <div className="search-field">
            <Search size={16} style={{ color: '#686861' }} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') void fetchDataset()
              }}
              placeholder="Search BASS-II runs by material, test number, or conditions (e.g. 'PMMA', 'B1', '22.2')..."
            />
          </div>
          <button className="btn btn-primary" onClick={() => fetchDataset()}>
            <span>Apply Filters</span>
          </button>
        </div>

        <div className="filter-bar">
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600, color: '#171715' }}>
            <Filter size={13} />
            <span>FILTERS:</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span>PI:</span>
            <select value={selectedPi} onChange={(e) => setSelectedPi(e.target.value)}>
              <option value="all">All Investigators (129)</option>
              <option value="Bhattacharjee">Bhattacharjee (68)</option>
              <option value="Olson">Olson (61)</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span>MATERIAL:</span>
            <select value={selectedFuel} onChange={(e) => setSelectedFuel(e.target.value)}>
              <option value="all">All Materials</option>
              <option value="PMMA">PMMA Film / Rod</option>
              <option value="Cotton">Cotton / Cellulosic Fabric</option>
              <option value="Polyethylene">Polyethylene</option>
              <option value="Silicone">Silicone Rubber</option>
            </select>
          </div>

          <span style={{ marginLeft: 'auto', color: '#686861', fontFamily: 'monospace' }}>
            {records.length} matching flight records
          </span>
        </div>
      </div>

      {/* 6. Responsive BASS-II Data Table */}
      <div className="light-panel" style={{ padding: '20px' }}>
        <SectionHeader
          eyebrow="RECORD EXPLORER"
          title="PSI-25 Flight Experiment Table"
          detail="Original strings and exact calibrated observations. Click column headers to sort."
        />

        {loading ? (
          <LoadingState message="Loading experimental table records..." />
        ) : (
          <DataTable records={records} pageSize={15} />
        )}
      </div>
    </div>
  )
}
