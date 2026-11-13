/**
 * AeroGuard AI - Backend API TypeScript Contracts
 * Strictly mirrors existing FastAPI routes and Pydantic/dict structures.
 */

export interface HealthResponse {
  status: string
  service: string
}

export interface RootResponse {
  message: string
  project: string
  version: string
}

// BASS-II Models
export interface Bass2Summary {
  dataset_name: string
  record_count: number
  declared_record_count: number
  column_count: number
  pi_counts: Record<string, number>
  blank_cells: number
  literal_none_cells: number
  duplicate_identifiers: Array<{ PI: string; 'Test #': string }>
  quality_flags_count: number
  source_values_modified: boolean
  scientific_findings_verified: boolean
}

export interface RawBass2Record {
  PI: string
  'Test #': string
  Date: string
  GMT: string
  'Sample #': string
  'Fuel Sample Material': string
  'Flow restrictor': string
  'Fan display': string
  'Air display': string
  'Radiometer gain   (1000   250   50   10)': string
  'Total Frames Shot': string
  'Calibrated  initial O2 % by vol ': string
  'Calibrated final O2 % by vol': string
  'Initial CO2 % by vol': string
  'Final CO2 % by vol': string
  'Initial CO (ppm)': string
  'Final CO (ppm)': string
  [key: string]: string
}

export interface Bass2SearchResultItem {
  record: RawBass2Record
  source_type: string
  matched_terms: string[]
  relevance_score: number
  relevance_components?: Record<string, unknown>
  matching_reasons?: string[]
  ranking_contract?: Record<string, unknown>
}

export interface Bass2SearchResponse {
  query: string
  filters: {
    pi?: string | null
    fuel?: string | null
    initial_oxygen?: number | null
    final_oxygen?: number | null
    numeric_field?: string | null
    numeric_value?: number | null
    numeric_tolerance?: number
  }
  count: number
  results: Bass2SearchResultItem[]
  notice: string
}

// Research Extractive Evidence Brief Models
export interface RankingContract {
  contract_version?: string
  source_identity?: {
    group_key?: string
    source_id?: string
  }
  source_type?: string
  evidence_scope?: string
  lexical_score?: number
  duplicate_source?: boolean
  scientific_findings_verified?: boolean
  [key: string]: unknown
}

export interface EvidenceBriefItem {
  record_id: string
  record_origin: string
  import_origin?: string
  source_id: string
  nasa_id: string
  source_title: string
  citation_url?: string
  source_url?: string
  pdf_page_number?: number | null
  evidence_role: string
  evidence_modality: string
  research_context?: string
  context_requirement?: string
  classification_version?: string
  classification_review_status?: string
  source_review_status?: string
  evidence_type?: string
  scientific_findings_verified: boolean
  matched_query_terms: string[]
  query_match_score: number
  relevance_components?: Record<string, unknown>
  matching_reasons: string[]
  exact_source_excerpt: string
  ranking_contract?: RankingContract
  duplicate_source?: boolean
}

export interface EvidenceBriefResponse {
  engine: string
  engine_version: string
  query: string
  retrieval_method: string
  ranking_note: string
  summary: {
    overview: string
    candidate_passage_count: number
    source_document_count: number
    evidence_role_counts: Record<string, number>
    evidence_modality_counts: Record<string, number>
  }
  search_audit: {
    nasa_passages_examined: number
    primary_nasa_passages_examined: number
    supplemental_nasa_passages_examined: number
    eligible_role_counts: Record<string, number>
    all_nasa_role_counts: Record<string, number>
    result_limit: number
    matched_passage_count_before_display_limit: number
    distinct_sources_before_display: number
    source_diversification: string
  }
  results: EvidenceBriefItem[]
  limitations: string[]
}

// NASA Online Search Models
export interface OnlineResearchResultItem {
  title: string
  abstract: string
  nasa_id: string | number
  source_url: string
  source: string
  authors: Array<{ name: string; affiliation?: string }>
  publication_date?: string | null
  keywords: string[]
  subject_categories: string[]
  document_type?: string
  dissemination_status?: string
  document_available?: boolean
  center?: string
  verification_status: string
  evidence_type: string
  full_text_retrieved: boolean
  scientific_findings_verified: boolean
  review_status: string
  relevance_score: number
  matching_reasons: string[]
  retrieval_timestamp: string
  retrieved_at: string
  ranking_contract?: RankingContract
  duplicate_source?: boolean
  record_type?: string
  evidence_scope?: string
}

export interface OnlineSearchResponse {
  source: string
  source_type?: string
  query: string
  normalized_query?: string
  count: number
  results: OnlineResearchResultItem[]
  retrieval_timestamp?: string
  retrieved_at?: string
  original_query?: string
  nasa_query?: string
  fallback_attempted?: boolean
  fallback_reason?: string | null
  original_result_count?: number
  fallback_result_count?: number
  error?: string
}

// Combined Federated Search Response
export interface CombinedSearchResponse {
  query: string
  search_strategy: string
  fallback_triggered: boolean
  fallback_reason?: string[]
  missing_query_concepts?: string[]
  fallback_thresholds?: {
    minimum_local_passages: number
    minimum_distinct_local_sources: number
    minimum_relevance_score: number
    relevant_local_passages: number
  }
  local_evidence_brief: EvidenceBriefResponse
  online_search: {
    performed: boolean
    source: string
    query: string
    original_query: string
    nasa_query?: string
    fallback_attempted: boolean
    fallback_reason?: string | null
    original_result_count: number
    fallback_result_count: number
    count: number
    results: OnlineResearchResultItem[]
    content_scope: string
    status?: string
    error?: string
  }
  combined_sources: Record<string, {
    nasa_id?: string | number
    title?: string
    citation_url?: string
    source_presence: string[]
    local_passage_count: number
    local_record_ids: string[]
    local_pdf_pages: number[]
    local_evidence_roles: string[]
    local_evidence_modalities: string[]
    ntrs_metadata?: unknown
  }>
  conflict_report: {
    conflicts?: unknown[]
    count: number
    limitations?: string[]
  }
  counts: {
    local_passages_returned: number
    local_sources_returned: number
    online_metadata_records: number
    new_online_sources_discovered: number
    online_sources_merged_with_local: number
    unique_combined_sources: number
  }
  notices: string[]
}

// Reviewed Evidence Search
export interface ReviewedEvidenceItem {
  evidence_id: string
  title: string
  finding: string
  evidence_class: string
  nasa_id: string
  citation_url?: string
  pdf_page?: number
  experimental_conditions?: Record<string, unknown>
  scientific_findings_verified: boolean
  matched_terms?: string[]
  score?: number
}

export interface ReviewedEvidenceResponse {
  query: string
  count: number
  results: ReviewedEvidenceItem[]
  notice: string
}

// NASA Passage Search
export interface PassageSearchResultItem {
  passage_id: string
  nasa_id: string
  title: string
  text: string
  page_number?: number | null
  section?: string
  classification?: string
  confidence?: string
  matched_terms: string[]
  score: number
  ranking_contract?: RankingContract
}

export interface PassageSearchResponse {
  query: string
  filters: {
    nasa_id?: string | null
    classification?: string | null
  }
  count: number
  results: PassageSearchResultItem[]
  notice: string
}

// Research Insights Models
export interface ClaimInsight {
  claim_id?: string
  claim_text: string
  claim_type?: string
  section_name?: string
  page_numbers?: number[]
  source_id?: string
  nasa_id?: string
  source_url?: string
  source_title?: string
  source_type?: string
  evidence_classification?: string
  source_verification_status?: string
  review_status?: string
  scientific_findings_verified?: boolean
}

export interface StructuredFinding {
  finding_id?: string
  finding_type?: string
  description?: string
  fields?: Record<string, {
    values?: Array<{ value: unknown; raw_value: unknown; unit?: string | null }>
  }>
  provenance?: Record<string, unknown>
}

export interface PaperInsight {
  document_id: string
  nasa_id: string
  source_url?: string
  source_title: string
  source_type: string
  evidence_classification: string
  verification_status: string
  review_status: string
  scientific_findings_verified: boolean
  summary: {
    title?: string
    objective?: string
    claims: ClaimInsight[]
    key_findings?: string[]
  }
  claims: ClaimInsight[]
  structured_findings: StructuredFinding
  provenance: {
    source_document_id?: string
    nasa_id?: string
    source_url?: string
    page_numbers: number[]
    sections: string[]
    review_status?: string
  }
}

export interface ResearchInsightsResponse {
  schema_version: string
  query: string
  retrieval: {
    strategy?: string
    fallback_triggered?: boolean
    fallback_reason?: string[]
    missing_query_concepts?: string[]
    online_search?: Record<string, unknown>
    counts?: Record<string, number>
  }
  evidence: {
    paper_count: number
    claim_count: number
    papers: PaperInsight[]
    claims: ClaimInsight[]
  }
  conflict_report: {
    conflicts: Array<{
      topic?: string
      description?: string
      status?: string
      source_ids?: string[]
    }>
    count: number
    limitations: string[]
  }
  recommendation: string
  scientific_findings_verified: boolean
  notices: string[]
  limitations: string[]
}

// Research Comparison Models
export interface ConditionComparisonField {
  dimension: string
  status: 'exact_match' | 'partial_match' | 'mismatch' | 'unknown' | string
  first_source_values: Array<{ value: unknown; raw_value: unknown; unit?: string | null }>
  second_source_values: Array<{ value: unknown; raw_value: unknown; unit?: string | null }>
  missing_information: string[]
}

export interface ComparisonPair {
  first_source: {
    document_id: string
    nasa_id: string
    source_url?: string
    source_title: string
    source_type: string
    evidence_classification: string
    verification_status: string
    review_status: string
  }
  second_source: {
    document_id: string
    nasa_id: string
    source_url?: string
    source_title: string
    source_type: string
    evidence_classification: string
    verification_status: string
    review_status: string
  }
  overall_status: 'exact_match' | 'compatible' | 'partial_match' | 'mismatch' | 'unknown'
  condition_comparisons: ConditionComparisonField[]
  missing_information: string[]
  comparison_rationale: string
  independence_status: string
  scientific_findings_verified: boolean
}

export interface ResearchComparisonResponse {
  schema_version: string
  query: string
  retrieval: ResearchInsightsResponse['retrieval']
  evidence: ResearchInsightsResponse['evidence']
  comparison: {
    comparable_sources: ComparisonPair[]
    non_comparable_sources: ComparisonPair[]
    condition_comparisons: ComparisonPair[]
    comparison_limitations: string[]
    sources: Array<ComparisonPair['first_source']>
    scientific_findings_verified: boolean
  }
  conflicts: unknown[]
  research_gaps: Array<{
    gap_id?: string
    dimension?: string
    description: string
    sources_involved?: string[]
  }>
  suggested_research_questions: FollowUpResearchQuestion[]
  comparison_limitations: string[]
  recommendation: string
  scientific_findings_verified: boolean
}

export interface FollowUpResearchQuestion {
  question: string
  gap_ids: string[]
  supporting_source_ids: string[]
}

// Mission Intelligence Models
export interface MissionResearchBrief {
  brief_id?: string
  mission_context?: Record<string, unknown>
  executive_summary?: string
  applicability_assessment?: string
  identified_constraints?: string[]
  critical_gaps?: string[]
}

export interface MissionIntelligenceResponse {
  schema_version: string
  query: string
  mission_context: Record<string, unknown>
  retrieval: ResearchInsightsResponse['retrieval']
  evidence: ResearchInsightsResponse['evidence']
  comparison: ResearchComparisonResponse['comparison']
  conflicts: unknown[]
  research_gaps: ResearchComparisonResponse['research_gaps']
  suggested_research_questions: FollowUpResearchQuestion[]
  bass2_evidence: {
    dataset_available: boolean
    search_status: string
    applied_filters: Record<string, unknown>
    total_matching_records: number
    returned_records: Bass2SearchResultItem[]
    dataset_summary: Bass2Summary
    dataset_name: string
    source: string
    field_names: string[]
    condition_summary: {
      initial_oxygen_field: string
      final_oxygen_field: string
      available_condition_fields: string[]
    }
    limitations: string[]
    scientific_findings_verified: boolean
  }
  reviews: {
    records: ReviewItem[]
    accepted_review_present: boolean
    authentication_status: string
  }
  mission_research_brief: MissionResearchBrief
  conclusion: string
  scientific_findings_verified: boolean
  limitations: string[]
}

// Dashboard Mission Brief (GET /dashboard/mission-brief)
export interface DashboardMissionBriefResponse {
  project: string
  mission_scenario: {
    mission: string
    query: string
    fuel?: string | null
    oxygen_concentration?: string | null
    flow_condition?: string | null
    gravity_condition?: string | null
    environment?: string | null
  }
  retrieval: {
    method: string
    scenario_terms: string[]
    ranking_note: string
  }
  evidence: {
    experimental: EvidenceBriefItem[]
    simulation: EvidenceBriefItem[]
    reviewed_context: EvidenceBriefItem[]
    bass2_context: EvidenceBriefItem[]
  }
  comparison: {
    experimental_passage_count: number
    simulation_passage_count: number
    comparison_note: string
    supplied_conditions: Record<string, string>
    compatibility_status: string
  }
  recommendations: Array<{
    recommendation: string
    supporting_source_id?: string | null
    source_title?: string | null
    source_url?: string | null
    passage?: string | null
    evidence_type?: string | null
    experimental_conditions?: Record<string, string>
    applicability_limitations?: string
    evidence_strength: string
    review_status?: string
  }>
  safety_insights: Array<{
    topic: string
    observation: string
    source_record_ids: string[]
    status: string
  }>
  coverage: {
    total_store_records: number
    nasa_passage_role_inventory: Record<string, number>
    matched_experimental_passages: number
    matched_simulation_passages: number
  }
  limitations: string[]
}

// Reviews Models
export interface ReviewItem {
  review_id: string
  revision: number
  target_type: string
  target_id: string
  source_document_id?: string | null
  nasa_id?: string | null
  source_url?: string | null
  reviewer_id?: string | null
  reviewer_identity_status: string
  status: 'pending' | 'accepted' | 'rejected' | 'needs_correction' | 'insufficient_evidence' | string
  reviewer_decision?: string | null
  reviewer_notes?: string | null
  correction_notes?: string | null
  scientific_findings_verified: boolean
  evidence_scope?: string | null
  created_at: string
  updated_at: string
}

export interface ReviewsListResponse {
  count: number
  reviews: ReviewItem[]
}

export interface ReviewHistoryEntry {
  revision: number
  status: string
  reviewer_id?: string | null
  reviewer_decision?: string | null
  reviewer_notes?: string | null
  correction_notes?: string | null
  scientific_findings_verified: boolean
  evidence_scope?: string | null
  created_at: string
}

export interface ReviewHistoryResponse {
  review_id: string
  history: ReviewHistoryEntry[]
}

export interface ImportNasaResponse {
  success: boolean
  status: string
  nasa_id: string
  title?: string
  passage_count?: number
  imported_passages_count?: number
  manual_review_status?: string
  error?: string
}
