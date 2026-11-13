export * from './api'

export type EvidenceKind = 'Experimental' | 'Simulation' | 'Abstract' | 'Reviewed' | string
export type VerificationState = 'Metadata only' | 'Extracted passage' | 'Human reviewed' | 'Not verified' | string

export interface PreviewPaper {
  id: string
  title: string
  nasaId: string
  abstract: string
  evidence: EvidenceKind
  verification: VerificationState
  score: number
  source: string
  material: string
  oxygen: string
  page: string
}

export interface BassRecord {
  pi: string
  test: string
  material: string
  initialO2: string
  finalO2: string
  flow: string
  frames: string
  date: string
}

export interface Insight {
  title: string
  type: EvidenceKind
  status: VerificationState
  excerpt: string
  source: string
  page: string
}
