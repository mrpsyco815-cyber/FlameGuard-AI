type MediaBackgroundProps = {
  src: string
  alt: string
  className?: string
  position?: string
}

export function MediaBackground({ src, alt, className = '', position = 'center' }: MediaBackgroundProps) {
  return <div className={`media-background ${className}`} style={{ backgroundImage: `url("${src}")`, backgroundPosition: position }} role="img" aria-label={alt} />
}
