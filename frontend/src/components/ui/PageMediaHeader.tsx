import { type ReactNode, useState } from 'react'

interface PageMediaHeaderProps {
  image: string
  alt: string
  credit?: string
  children: ReactNode
}

export function PageMediaHeader({
  image,
  alt,
  credit,
  children,
}: PageMediaHeaderProps) {
  const [failed, setFailed] = useState(false)

  return (
    <div className="page-media-header" aria-label={alt}>
      {!failed && (
        <img
          src={image}
          alt={alt}
          className="page-media-image"
          onError={() => setFailed(true)}
        />
      )}
      <div className="page-media-overlay" />
      <div className="page-media-content">{children}</div>
      {credit && <div className="page-media-credit">{credit}</div>}
    </div>
  )
}
