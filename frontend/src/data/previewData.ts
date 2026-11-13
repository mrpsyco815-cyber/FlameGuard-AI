import type { BassRecord, Insight, PreviewPaper } from '../types'

export const previewLabel = 'ILLUSTRATIVE PREVIEW — NOT LIVE NASA DATA'

export const papers: PreviewPaper[] = [
  {
    id: 'paper-01',
    title: 'Flame spread behavior over solid fuels in reduced gravity',
    nasaId: 'PREVIEW-NASA-0001',
    abstract: 'Preview abstract: a source-linked passage would appear here after backend integration, with conditions retained exactly as reported.',
    evidence: 'Experimental',
    verification: 'Extracted passage',
    score: 0.94,
    source: 'NASA NTRS preview',
    material: 'PMMA',
    oxygen: '21% O₂',
    page: 'p. 14',
  },
  {
    id: 'paper-02',
    title: 'Radiative effects in microgravity combustion experiments',
    nasaId: 'PREVIEW-NASA-0002',
    abstract: 'Preview abstract: this card demonstrates abstract-only evidence and must not be read as a verified scientific conclusion.',
    evidence: 'Abstract',
    verification: 'Metadata only',
    score: 0.82,
    source: 'NASA NTRS preview',
    material: 'Cellulosic',
    oxygen: '25% O₂',
    page: 'Abstract',
  },
  {
    id: 'paper-03',
    title: 'Numerical study of oxygen concentration and flame extinction',
    nasaId: 'PREVIEW-NASA-0003',
    abstract: 'Preview abstract: simulation results are kept distinct from direct experimental observations.',
    evidence: 'Simulation',
    verification: 'Not verified',
    score: 0.71,
    source: 'NASA NTRS preview',
    material: 'Polyethylene',
    oxygen: '18% O₂',
    page: 'p. 22',
  },
]

export const bassRecords: BassRecord[] = [
  { pi: 'Bhattacharjee', test: 'B1', material: '100 micron PMMA film', initialO2: '20.94', finalO2: '20.61', flow: '2', frames: '250', date: '2/19/2014' },
  { pi: 'Olson', test: 'C7', material: 'Cellulose paper', initialO2: '25.00', finalO2: '24.38', flow: '1', frames: '480', date: '3/04/2014' },
  { pi: 'Bhattacharjee', test: 'D3', material: 'Polyethylene film', initialO2: '18.02', finalO2: '17.74', flow: '3', frames: '320', date: '3/18/2014' },
  { pi: 'Olson', test: 'F2', material: '100 micron PMMA film', initialO2: '30.10', finalO2: '29.55', flow: '2', frames: '180', date: '4/02/2014' },
  { pi: 'Zhou', test: 'G9', material: 'Silicone rubber', initialO2: '21.10', finalO2: '20.98', flow: '0', frames: '120', date: '4/14/2014' },
]

export const insights: Insight[] = [
  { title: 'Oxygen condition is explicitly reported in the source excerpt', type: 'Experimental', status: 'Extracted passage', excerpt: 'Preview excerpt: reported oxygen conditions would be shown with page and section provenance.', source: 'PREVIEW-NASA-0001', page: 'p. 14' },
  { title: 'Catalogue metadata is not a full-text finding', type: 'Abstract', status: 'Metadata only', excerpt: 'Preview excerpt: abstract evidence remains bibliographic scope until source text is retrieved.', source: 'PREVIEW-NASA-0002', page: 'Abstract' },
  { title: 'Model output requires separate interpretation', type: 'Simulation', status: 'Not verified', excerpt: 'Preview excerpt: simulation and experimental observations must not be combined into one claim.', source: 'PREVIEW-NASA-0003', page: 'p. 22' },
]

export const evidenceDistribution = [
  { name: 'Experimental', value: 42, color: '#42d8ff' },
  { name: 'Simulation', value: 26, color: '#8b7bff' },
  { name: 'Abstract', value: 22, color: '#f2b84b' },
  { name: 'Reviewed', value: 10, color: '#65e6a3' },
]

export const oxygenTrend = [
  { test: 'B1', initial: 20.94, final: 20.61 },
  { test: 'C7', initial: 25, final: 24.38 },
  { test: 'D3', initial: 18.02, final: 17.74 },
  { test: 'F2', initial: 30.1, final: 29.55 },
  { test: 'G9', initial: 21.1, final: 20.98 },
]

export const activity = [
  ['11:42', 'NASA catalogue query staged', 'NASA Research'],
  ['10:18', 'BASS-II preview records filtered', 'BASS-II Data'],
  ['09:52', 'Comparison matrix prepared', 'Research Comparison'],
  ['08:36', 'Human review status panel opened', 'Mission Intelligence'],
]
