import { useEffect, useState } from 'react'
import { ArrowRight, Compass, FileSearch, Globe2 } from 'lucide-react'
import { Link } from 'react-router-dom'

export type ReelType = 'orbital'

interface VideoReel {
  id: ReelType
  label: string
  shortLabel: string
  resolution: string
  badge: string
  videoSrc: string
  posterSrc: string
  credit: string
  alt: string
  icon: typeof Globe2
}

const REELS: Record<ReelType, VideoReel> = {
  orbital: {
    id: 'orbital',
    label: 'Earth Orbit (720p)',
    shortLabel: 'Earth Orbit',
    resolution: '1280 × 720 HD',
    badge: 'NASA HDEV · Earth Observation Platform',
    videoSrc: '/media/videos/earth-views-iss-medium.mp4',
    posterSrc: '/media/posters/earth-views-iss.jpg',
    credit: 'NASA High Definition Earth Viewing (HDEV) · International Space Station',
    alt: 'Earth views from the International Space Station HDEV external camera platform',
    icon: Globe2,
  },
}

export function CinematicHero() {
  const [activeReel, setActiveReel] = useState<ReelType>('orbital')
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false)
  const [videoError, setVideoError] = useState(false)

  const reel = REELS[activeReel]

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    setPrefersReducedMotion(mediaQuery.matches)
    const listener = (e: MediaQueryListEvent) => setPrefersReducedMotion(e.matches)
    mediaQuery.addEventListener('change', listener)
    return () => mediaQuery.removeEventListener('change', listener)
  }, [])

  return (
    <section className="hero-video-container" aria-label="AeroGuard AI Dashboard Hero">
      {!prefersReducedMotion && !videoError ? (
        <video
          key={reel.videoSrc}
          className="hero-video"
          autoPlay
          muted
          loop
          playsInline
          poster={reel.posterSrc}
          onError={() => setVideoError(true)}
          aria-label={reel.alt}
        >
          <source src={reel.videoSrc} type="video/mp4" />
          <img
            src={reel.posterSrc}
            alt={`${reel.alt} fallback poster`}
            className="hero-video"
          />
        </video>
      ) : (
        <img
          src={reel.posterSrc}
          alt={reel.alt}
          className="hero-video"
        />
      )}

      <div className="hero-video-overlay" />

      {/* Reel switcher toolbar with authentic real NASA video streams */}
      <div className="hero-reel-switcher" role="toolbar" aria-label="NASA Video Stream Switcher">
        {(Object.keys(REELS) as ReelType[]).map((key) => {
          const r = REELS[key]
          const Icon = r.icon
          const isActive = activeReel === key
          return (
            <button
              key={key}
              type="button"
              onClick={() => {
                setActiveReel(key)
                setVideoError(false)
              }}
              className={`hero-reel-btn ${isActive ? 'hero-reel-active' : ''}`}
              aria-pressed={isActive}
              title={`Switch to ${r.label}`}
            >
              <Icon size={12} />
              <span>{r.shortLabel}</span>
            </button>
          )
        })}
      </div>

      <div className="hero-content">
        <div className="eyebrow eyebrow-dark">
          <span>{reel.badge}</span>
        </div>
        <h1>
          Microgravity Combustion <em>Intelligence.</em>
        </h1>
        <p>
          Evidence-grounded research intelligence for spacecraft fire safety and spaceflight
          combustion physics. Synthesizing NASA Technical Reports Server documents, PSI-25
          BASS-II experimental data, and multi-mission environmental matrices (Spacecraft, Lunar, Martian).
        </p>

        <div className="hero-actions">
          <Link
            to="/research"
            className="btn btn-primary"
            style={{ backgroundColor: '#151515', color: '#FFFFFF', border: '1px solid rgba(255,255,255,0.2)' }}
          >
            <FileSearch size={15} />
            <span>Search NASA Evidence</span>
            <ArrowRight size={14} />
          </Link>
          <Link to="/mission-intelligence" className="btn btn-secondary">
            <Compass size={15} />
            <span>Mission Intelligence</span>
          </Link>
        </div>
      </div>

      <div className="hero-credit">
        {reel.credit} · Native: {reel.resolution}
      </div>
    </section>
  )
}
