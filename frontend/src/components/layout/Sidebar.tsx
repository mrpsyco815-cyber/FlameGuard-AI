import { useEffect, useState } from 'react'
import { NavLink } from 'react-router-dom'
import {
  Compass,
  Database,
  FileSearch,
  FlaskConical,
  GitCompare,
  LayoutDashboard,
  ShieldCheck,
  X,
} from 'lucide-react'
import { api } from '../../api/client'

const navigationLinks = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/research', label: 'NASA Research', icon: FileSearch },
  { to: '/bass2', label: 'BASS-II Data', icon: Database },
  { to: '/insights', label: 'Research Insights', icon: FlaskConical },
  { to: '/comparison', label: 'Research Comparison', icon: GitCompare },
  { to: '/mission-intelligence', label: 'Mission Intelligence', icon: Compass },
]

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const [backendHealthy, setBackendHealthy] = useState<boolean | null>(null)

  useEffect(() => {
    let mounted = true
    const checkHealth = async () => {
      try {
        const res = await api.getHealth()
        if (mounted) setBackendHealthy(res.status === 'healthy')
      } catch {
        if (mounted) setBackendHealthy(false)
      }
    }
    void checkHealth()
    const interval = setInterval(() => void checkHealth(), 30000)
    return () => {
      mounted = false
      clearInterval(interval)
    }
  }, [])

  return (
    <>
      {/* Mobile backdrop scrim */}
      <div
        className={`sidebar-scrim ${isOpen ? 'sidebar-scrim-visible' : ''}`}
        onClick={onClose}
        aria-hidden={!isOpen}
      />

      <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`} aria-label="Main Navigation">
        <div className="brand-row">
          <div className="brand-mark">
            <ShieldCheck size={20} strokeWidth={2.2} />
          </div>
          <div className="brand-title">
            <strong>AEROGUARD AI</strong>
            <span>Microgravity Combustion Intelligence</span>
          </div>
          <button
            type="button"
            className="sidebar-close-btn"
            onClick={onClose}
            aria-label="Close navigation menu"
          >
            <X size={18} />
          </button>
        </div>

        <div className="nav-section-label">Research Intelligence</div>

        <nav className="nav-list" aria-label="Primary navigation">
          {navigationLinks.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              onClick={onClose}
              className={({ isActive }) => `nav-item ${isActive ? 'nav-active' : ''}`}
            >
              <Icon size={16} strokeWidth={1.8} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-foot">
          <div className="system-status">
            <span
              className={backendHealthy ? 'status-dot-active' : 'status-dot-offline'}
            />
            <span>
              {backendHealthy === null
                ? 'CHECKING SYSTEM...'
                : backendHealthy
                ? 'API CONNECTED (PORT 8000)'
                : 'API OFFLINE / TIMEOUT'}
            </span>
          </div>
          <span className="sidebar-version">
            AEROGUARD v0.1.0 · EVIDENCE-GROUNDED
          </span>
        </div>
      </aside>
    </>
  )
}
