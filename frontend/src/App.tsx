import { Routes, Route } from 'react-router-dom'
import { AppLayout } from './components/layout/AppLayout'
import Dashboard from './pages/Dashboard'
import NasaResearch from './pages/NasaResearch'
import Bass2Data from './pages/Bass2Data'
import ResearchInsights from './pages/ResearchInsights'
import ResearchComparison from './pages/ResearchComparison'
import MissionIntelligence from './pages/MissionIntelligence'

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/research" element={<NasaResearch />} />
        <Route path="/bass2" element={<Bass2Data />} />
        <Route path="/insights" element={<ResearchInsights />} />
        <Route path="/comparison" element={<ResearchComparison />} />
        <Route path="/mission-intelligence" element={<MissionIntelligence />} />
      </Route>
    </Routes>
  )
}
