/**
 * AeroGuard AI - Centralized API Service Layer
 * Single point of network communication for all frontend modules.
 */

import type {
  Bass2SearchResponse,
  Bass2Summary,
  CombinedSearchResponse,
  DashboardMissionBriefResponse,
  EvidenceBriefResponse,
  HealthResponse,
  MissionIntelligenceResponse,
  OnlineSearchResponse,
  PassageSearchResponse,
  ResearchComparisonResponse,
  ResearchInsightsResponse,
  ReviewedEvidenceResponse,
  ReviewHistoryResponse,
  ReviewItem,
  ReviewsListResponse,
  ImportNasaResponse,
} from '../types/api'

// Base URL: In browser dev, prefer '/api' so Vite proxy forwards to backend avoiding CORS
const RAW_BASE_URL = import.meta.env.VITE_API_BASE_URL
export const API_BASE_URL = RAW_BASE_URL && RAW_BASE_URL.trim() !== ''
  ? RAW_BASE_URL.replace(/\/+$/, '')
  : '/api'

const DEFAULT_TIMEOUT_MS = 25000

export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details?: unknown
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {},
  timeoutMs: number = DEFAULT_TIMEOUT_MS
): Promise<T> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs)

  const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Accept': 'application/json',
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      let errorDetail: unknown = null
      try {
        errorDetail = await response.json()
      } catch {
        errorDetail = await response.text()
      }
      const message = typeof errorDetail === 'object' && errorDetail !== null && 'detail' in errorDetail
        ? String((errorDetail as { detail: unknown }).detail)
        : `Request failed with status ${response.status} ${response.statusText}`
      throw new ApiError(message, response.status, errorDetail)
    }

    return await response.json() as T
  } catch (err: unknown) {
    clearTimeout(timeoutId)
    if (err instanceof ApiError) {
      throw err
    }
    if (err instanceof Error) {
      if (err.name === 'AbortError') {
        throw new ApiError(`Request timeout after ${timeoutMs / 1000}s. Check backend connectivity.`, 408)
      }
      throw new ApiError(err.message)
    }
    throw new ApiError('An unexpected network error occurred.')
  }
}

export const api = {
  // System Health
  async getHealth(): Promise<HealthResponse> {
    return request<HealthResponse>('/health', { method: 'GET' }, 5000)
  },

  // BASS-II Endpoints
  async getBass2Summary(): Promise<Bass2Summary> {
    return request<Bass2Summary>('/bass2/summary', { method: 'GET' })
  },

  async searchBass2(params: {
    q?: string
    limit?: number
    pi?: string
    fuel?: string
    initial_oxygen?: number
    final_oxygen?: number
    numeric_field?: string
    numeric_value?: number
    numeric_tolerance?: number
  } = {}): Promise<Bass2SearchResponse> {
    const query = new URLSearchParams()
    if (params.q) query.set('q', params.q)
    if (params.limit) query.set('limit', String(params.limit))
    if (params.pi) query.set('pi', params.pi)
    if (params.fuel) query.set('fuel', params.fuel)
    if (params.initial_oxygen !== undefined && params.initial_oxygen !== null) {
      query.set('initial_oxygen', String(params.initial_oxygen))
    }
    if (params.final_oxygen !== undefined && params.final_oxygen !== null) {
      query.set('final_oxygen', String(params.final_oxygen))
    }
    if (params.numeric_field) query.set('numeric_field', params.numeric_field)
    if (params.numeric_value !== undefined && params.numeric_value !== null) {
      query.set('numeric_value', String(params.numeric_value))
    }
    if (params.numeric_tolerance !== undefined && params.numeric_tolerance !== null) {
      query.set('numeric_tolerance', String(params.numeric_tolerance))
    }
    return request<Bass2SearchResponse>(`/bass2/search?${query.toString()}`, { method: 'GET' })
  },

  // Extractive Evidence Brief Search
  async searchResearch(query: string, limit: number = 10): Promise<EvidenceBriefResponse> {
    const params = new URLSearchParams({ q: query, limit: String(limit) })
    return request<EvidenceBriefResponse>(`/research/search?${params.toString()}`, { method: 'GET' })
  },

  // Online NASA NTRS Search
  async searchOnlineResearch(query: string, limit: number = 5): Promise<OnlineSearchResponse> {
    const params = new URLSearchParams({ q: query, limit: String(limit) })
    return request<OnlineSearchResponse>(`/research/online-search?${params.toString()}`, { method: 'GET' })
  },

  // Combined Federated Search (Local-First with NTRS Fallback)
  async searchCombinedResearch(query: string, limit: number = 8): Promise<CombinedSearchResponse> {
    const params = new URLSearchParams({ q: query, limit: String(limit) })
    return request<CombinedSearchResponse>(`/research/combined-search?${params.toString()}`, { method: 'GET' })
  },

  // Reviewed Evidence Search
  async searchEvidence(query: string, limit: number = 10): Promise<ReviewedEvidenceResponse> {
    const params = new URLSearchParams({ q: query, limit: String(limit) })
    return request<ReviewedEvidenceResponse>(`/research/evidence-search?${params.toString()}`, { method: 'GET' })
  },

  // NASA Passage Search
  async searchPassages(params: {
    q?: string
    limit?: number
    nasa_id?: string
    classification?: string
  } = {}): Promise<PassageSearchResponse> {
    const query = new URLSearchParams()
    if (params.q) query.set('q', params.q)
    if (params.limit) query.set('limit', String(params.limit))
    if (params.nasa_id) query.set('nasa_id', params.nasa_id)
    if (params.classification) query.set('classification', params.classification)
    return request<PassageSearchResponse>(`/research/nasa-passage-search?${query.toString()}`, { method: 'GET' })
  },

  // Research Insights
  async getResearchInsights(query: string, limit: number = 10): Promise<ResearchInsightsResponse> {
    return request<ResearchInsightsResponse>('/research/insights', {
      method: 'POST',
      body: JSON.stringify({ query, limit }),
    })
  },

  // Research Comparison
  async getResearchComparison(query: string, limit: number = 10): Promise<ResearchComparisonResponse> {
    return request<ResearchComparisonResponse>('/research/insights/compare', {
      method: 'POST',
      body: JSON.stringify({ query, limit }),
    })
  },

  // Mission Intelligence Orchestration
  async getMissionIntelligence(payload: {
    query: string
    mission_context?: Record<string, unknown>
    limit?: number
    review_status?: string
  }): Promise<MissionIntelligenceResponse> {
    return request<MissionIntelligenceResponse>('/research/mission-intelligence', {
      method: 'POST',
      body: JSON.stringify({
        query: payload.query,
        mission_context: payload.mission_context || {},
        limit: payload.limit || 10,
        review_status: payload.review_status,
      }),
    })
  },

  // Dashboard Mission Brief
  async getDashboardMissionBrief(params: {
    mission: 'moon' | 'mars' | 'spacecraft'
    q: string
    fuel?: string
    oxygen_concentration?: string
    flow_condition?: string
    gravity_condition?: string
    environment?: string
    limit?: number
  }): Promise<DashboardMissionBriefResponse> {
    const query = new URLSearchParams({
      mission: params.mission,
      q: params.q,
    })
    if (params.fuel) query.set('fuel', params.fuel)
    if (params.oxygen_concentration) query.set('oxygen_concentration', params.oxygen_concentration)
    if (params.flow_condition) query.set('flow_condition', params.flow_condition)
    if (params.gravity_condition) query.set('gravity_condition', params.gravity_condition)
    if (params.environment) query.set('environment', params.environment)
    if (params.limit) query.set('limit', String(params.limit))

    return request<DashboardMissionBriefResponse>(`/dashboard/mission-brief?${query.toString()}`, { method: 'GET' })
  },

  // Human Reviews
  async getReviews(params: {
    target_type?: string
    target_id?: string
    status?: string
    limit?: number
  } = {}): Promise<ReviewsListResponse> {
    const query = new URLSearchParams()
    if (params.target_type) query.set('target_type', params.target_type)
    if (params.target_id) query.set('target_id', params.target_id)
    if (params.status) query.set('status', params.status)
    if (params.limit) query.set('limit', String(params.limit))
    return request<ReviewsListResponse>(`/research/reviews?${query.toString()}`, { method: 'GET' })
  },

  async getReview(reviewId: string): Promise<ReviewItem> {
    return request<ReviewItem>(`/research/reviews/${encodeURIComponent(reviewId)}`, { method: 'GET' })
  },

  async createReview(payload: {
    target_type: string
    target_id: string
    status?: string
    source_document_id?: string
    nasa_id?: string
    source_url?: string
    reviewer_id?: string
    reviewer_decision?: string
    reviewer_notes?: string
    correction_notes?: string
    scientific_findings_verified?: boolean
    evidence_scope?: string
  }): Promise<ReviewItem> {
    return request<ReviewItem>('/research/reviews', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  async updateReview(
    reviewId: string,
    payload: {
      status?: string
      reviewer_id?: string
      reviewer_decision?: string
      reviewer_notes?: string
      correction_notes?: string
      scientific_findings_verified?: boolean
      evidence_scope?: string
      [key: string]: unknown
    }
  ): Promise<ReviewItem> {
    return request<ReviewItem>(`/research/reviews/${encodeURIComponent(reviewId)}`, {
      method: 'PATCH',
      body: JSON.stringify(payload),
    })
  },

  async getReviewHistory(reviewId: string): Promise<ReviewHistoryResponse> {
    return request<ReviewHistoryResponse>(`/research/reviews/${encodeURIComponent(reviewId)}/history`, {
      method: 'GET',
    })
  },

  async importNasaDocument(nasaId: string): Promise<ImportNasaResponse> {
    return request<ImportNasaResponse>(`/research/import/${encodeURIComponent(nasaId)}`, {
      method: 'POST',
    })
  },
}

