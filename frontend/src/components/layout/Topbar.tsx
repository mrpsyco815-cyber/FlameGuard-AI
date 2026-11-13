import { useEffect, useState } from 'react'
import { Menu, Server, Shield } from 'lucide-react'
import { api } from '../../api/client'

interface TopbarProps {
  onOpenMobileNav?: () => void
}

export function Topbar({ onOpenMobileNav }: TopbarProps) {
  const [apiConnected, setApiConnected] = useState<boolean | null>(null)

  useEffect(() => {
    let mounted = true
    api.getHealth()
      .then((res) => {
        if (mounted) setApiConnected(res.status === 'healthy')
      })
      .catch(() => {
        if (mounted) setApiConnected(false)
      })
    return () => {
      mounted = false
    }
  }, [])

  return (
    <header className="topbar">
      <div className="topbar-left">
        <button
          type="button"
          className="mobile-menu-trigger"
          onClick={onOpenMobileNav}
          aria-label="Open navigation menu"
        >
          <Menu size={18} />
        </button>

        <div className="breadcrumb">
          <span className="breadcrumb-brand">AEROGUARD AI</span>
          <span className="breadcrumb-divider">/</span>
          <b className="breadcrumb-sub">MICROGRAVITY COMBUSTION INTELLIGENCE</b>
        </div>
      </div>

      <div className="topbar-actions">
        <div className="topbar-badge" title="FastAPI server connection state on port 8000">
          <Server size={13} style={{ color: apiConnected ? '#3D6B49' : '#A64B3E', flexShrink: 0 }} />
          <span className="topbar-badge-text-full">
            {apiConnected === null
              ? 'CONNECTING...'
              : apiConnected
              ? 'BACKEND: ACTIVE'
              : 'BACKEND: DISCONNECTED'}
          </span>
          <span className="topbar-badge-text-short">
            {apiConnected === null ? 'SYNC' : apiConnected ? 'ACTIVE' : 'OFFLINE'}
          </span>
        </div>

        <div className="topbar-badge topbar-badge-protocol" title="Research-support interface; not a certified fire safety authority">
          <Shield size={13} style={{ color: '#D96C32', flexShrink: 0 }} />
          <span className="topbar-badge-text-full">RESEARCH PROTOCOL</span>
          <span className="topbar-badge-text-short">PROTOCOL</span>
        </div>
      </div>
    </header>
  )
}
