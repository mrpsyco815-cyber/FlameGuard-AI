# AeroGuard AI Frontend Phase 1 Implementation Plan

## 1. Scope and implementation status

This document defines the architecture for the first frontend implementation.
It is a plan only. No frontend or backend implementation was started as part
of this phase.

The plan is based on:

- [FRONTEND_HANDOVER.md](./FRONTEND_HANDOVER.md)
- [FRONTEND_API_CONTRACT.md](./FRONTEND_API_CONTRACT.md)
- The current repository structure and README.

### Current repository finding

There is currently **no frontend application** in the repository:

- No `frontend/` directory.
- No `src/` directory.
- No `package.json`.
- No TypeScript configuration.
- No existing component library, router, state library, or CSS framework.
- The repository currently contains a Python/FastAPI backend, tests, research
  data, and documentation.

Therefore, there are no existing frontend dependencies or components to reuse.
The framework and dependency choices below are recommendations requiring review
before implementation.

## 2. Proposed frontend architecture

### Recommended baseline

Use a TypeScript React single-page application with:

- A route-based application shell.
- A typed API client using the browser `fetch` API initially.
- Feature-local components and types.
- CSS variables and component styles rather than introducing a design system
  dependency before the visual direction is approved.
- Native `AbortController` for request cancellation.

This is a recommendation, not an installed dependency decision. No packages
should be installed until the framework choice, deployment model, and CORS
strategy are approved.

### Suggested directory structure

```text
frontend/
  index.html
  package.json
  tsconfig.json
  src/
    app/
      App.tsx
      routes.tsx
      AppShell.tsx
    api/
      client.ts
      errors.ts
      endpoints.ts
      types.ts
    components/
      layout/
      feedback/
      provenance/
      evidence/
      search/
      comparison/
      mission/
      dataset/
      review/
    features/
      overview/
      research/
      nasa/
      bass2/
      comparison/
      mission-intelligence/
      reviews/
    styles/
      tokens.css
      globals.css
    lib/
      formatting.ts
      validation.ts
```

The exact top-level location (`frontend/` versus repository root) is a
project-level decision. A separate `frontend/` directory is recommended to
keep Python backend and JavaScript tooling isolated.

## 3. Page structure and navigation

### Primary navigation

1. **Overview**
   - Service health and API availability.
   - Research workflow entry points.
   - Visible scientific-use disclaimer.
2. **Research Search**
   - Unified local-first research search.
   - Search results, evidence excerpts, provenance, and NASA fallback state.
3. **NASA Catalogue**
   - NASA NTRS metadata search.
   - Extracted passage search.
   - Reviewed evidence search.
   - Import action only if explicitly approved for a privileged workflow.
4. **BASS-II Dataset**
   - Dataset summary.
   - Search/filterable original records.
   - Exact source fields and dataset limitations.
5. **Compare & Gaps**
   - Research insights comparison.
   - Condition comparison, conflicts, research gaps, and questions.
6. **Mission Intelligence**
   - Review-aware mission research workflow.
   - Mission context, evidence applicability, BASS-II context, and reviews.
7. **Human Review**
   - Review list, review detail, revision history, and status updates.

### Routes

Suggested client routes:

```text
/
/research
/nasa
/bass2
/compare
/mission-intelligence
/reviews
/reviews/:reviewId
/about-limitations
```

These are frontend routes only. They do not imply additional backend
endpoints.

## 4. Component hierarchy

```text
App
└── AppShell
    ├── SkipLink
    ├── Header
    │   ├── Brand
    │   ├── BackendStatusIndicator
    │   └── ResponsiveNavigation
    ├── Main
    │   └── RoutedPage
    └── Footer
        └── ScientificUseNotice
```

### Shared feedback components

- `LoadingState`
  - Shows operation name and cancellation affordance for long NASA requests.
- `ErrorState`
  - Distinguishes HTTP 400, 404, 422, 502, and 503.
  - Displays backend `detail` when present.
- `EmptyState`
  - States whether no records matched, no filters were supplied, or the
    backend returned no data.
- `InsufficientEvidenceState`
  - Uses the backend's conservative recommendation and limitations.
- `NoticeBanner`
  - Displays metadata-only, heuristic, unverified, or review-required notices.
- `SkeletonCard` / `SkeletonTable`
  - Prevents layout shift during asynchronous requests.

### Shared scientific components

- `ProvenancePanel`
  - NASA/document ID, source URL, title, page numbers, sections, and source
    type.
- `VerificationBadge`
  - Displays `scientific_findings_verified`, `verification_status`, and
    `review_status` separately.
- `EvidenceTypeBadge`
  - Experimental result, simulation, interpretation, limitation, abstract,
    metadata, or BASS-II metadata.
- `SourceExcerpt`
  - Exact supporting excerpt/text; never paraphrases as a verified finding.
- `ConditionSummary`
  - Reported values, raw values, units, and unknown fields.
- `RankingExplanation`
  - Lexical matching and ranking metadata with a clear non-confidence label.
- `LimitationsPanel`
  - Renders endpoint notices and limitations without collapsing them by
    default.

### Feature components

- `ResearchQueryForm`, `ResearchResultList`, `PaperCard`, `ClaimCard`,
  `StructuredFindingsPanel`
- `NASAOnlineSearchForm`, `NASARecordCard`, `PassageSearchPanel`,
  `ReviewedEvidenceCard`
- `Bass2SummaryCards`, `Bass2FilterForm`, `Bass2RecordTable`,
  `RawRecordDrawer`
- `ComparisonMatrix`, `ConflictList`, `ResearchGapList`,
  `SuggestedQuestionList`
- `MissionContextForm`, `MissionEvidenceSummary`, `MissionBriefTable`,
  `Bass2MissionContext`, `ReviewPresencePanel`
- `ReviewTable`, `ReviewEditor`, `ReviewHistory`

## 5. API-to-screen mapping

| Frontend feature | Backend endpoint | Method | Primary use |
|---|---|---:|---|
| Service status | `/health` | GET | Overview status indicator |
| API identity | `/` | GET | Diagnostics/about |
| Unified research | `/research/insights` | POST | Research Search |
| Condition comparison | `/research/insights/compare` | POST | Compare & Gaps |
| Review-aware mission workflow | `/research/mission-intelligence` | POST | Mission Intelligence |
| NASA catalogue search | `/research/online-search` | GET | NASA Catalogue |
| Local-first federation | `/research/combined-search` | GET | Research fallback details |
| Local evidence brief | `/research/search` | GET | Advanced/local search |
| Extracted NASA passages | `/research/nasa-passage-search` | GET | NASA Catalogue |
| Reviewed evidence | `/research/evidence-search` | GET | NASA Catalogue |
| BASS-II summary | `/bass2/summary` | GET | BASS-II Dataset |
| BASS-II records | `/bass2/search` | GET | BASS-II Dataset |
| Legacy mission dashboard | `/dashboard/mission-brief` | GET | Compatibility/optional |
| Create review | `/research/reviews` | POST | Human Review |
| List reviews | `/research/reviews` | GET | Human Review |
| Review detail | `/research/reviews/:id` | GET | Human Review |
| Review history | `/research/reviews/:id/history` | GET | Human Review |
| Update review | `/research/reviews/:id` | PATCH | Human Review |
| NASA document import | `/research/import/:nasaId` | POST | Privileged workflow only |

The import endpoint is intentionally not part of the default public
navigation. It mutates backend data and can download/extract an external PDF.

## 5A. Security architecture and final approval corrections

This section is a planning decision only. It does not authorize implementation,
database changes, Supabase configuration, or environment-variable changes.

### Authentication boundary

The browser will use Supabase Auth through a same-origin backend/BFF boundary
in production. The backend, not the browser, is responsible for converting the
authenticated request into a verified application identity and for enforcing
authorization. Frontend route guards are UX only and are never security
controls.

#### Authentication lifecycle

The production BFF flow is:

1. The browser starts login through the same-origin BFF. The BFF redirects to
   the approved Supabase Auth flow and receives the callback authorization code
   over HTTPS. Tokens are exchanged server-to-server; the browser does not
   receive a refresh token.
2. Before creating an application session, the BFF verifies the returned
   access JWT using the configured issuer, JWKS, algorithm, audience, issuer,
   expiry, not-before, and signature rules below. A failed verification never
   creates a cookie.
3. The BFF stores the refresh session server-side, protected by the approved
   secret/encryption and session-store controls, and issues an opaque session
   cookie. The cookie maps to the server-side session; it is not a JWT.
4. On reload or browser restart, the browser sends the still-valid cookie to
   the BFF. The BFF restores the server-side session and checks its expiry and
   revocation state. It does not trust browser route state as proof of login.
5. Before access expiry, the BFF refreshes the Supabase session server-side.
   Refresh-token rotation replaces the stored refresh token atomically. A
   refresh-token reuse or rotation failure revokes the affected session and
   requires login again.
6. Logout revokes the Supabase refresh session where supported, deletes the
   server-side session, and expires the browser cookie. Administrative
   revocation also invalidates matching server sessions without waiting for
   the original access token to expire.

The production cookie is a host-only cookie such as
`__Host-aeroguard_session`: `Secure`, `HttpOnly`, `SameSite=Lax`, `Path=/`,
an explicit idle and absolute lifetime, and no `Domain` attribute. Cookie
scope is limited to the BFF origin; cross-site credentialed requests are not
enabled. State-changing requests also require a CSRF token delivered by a
same-origin endpoint or the initial application response and returned in an
`X-CSRF-Token` header. The BFF validates the token, the session binding, and
the expected `Origin` (or an approved `Referer`) before processing the
request. Safe read-only requests do not change state.

Development has a separate, explicitly non-production flow: a direct browser
Supabase JS client may hold the session using its documented storage setting
and send an access token in an `Authorization: Bearer` header to a local
backend over the approved development origin. The local backend still
verifies the JWT on every request, but it does not issue production BFF
cookies or use production secrets/data. Development may set
`persistSession: false` to avoid persistence, or may use the SDK default
`localStorage` persistence only when that risk is explicitly accepted. This
bearer-token flow must not be described as the production session design.

#### Token storage decision

Supabase JS persists a browser session by default: `persistSession` is true,
and its default storage adapter is browser `localStorage` when available. That
means the access token and refresh-token session can survive page reloads and
browser restarts. The plan must not describe this default as avoiding
`localStorage`.

Storage options:

| Option | XSS exposure | CSRF exposure | Refresh and persistence implications |
|---|---|---|---|
| `localStorage` | JavaScript can read tokens after XSS; a token can be exfiltrated | Bearer header use is not automatically sent cross-site, but an XSS attacker can use it | Default Supabase persistence; survives reload/restart until sign-out or expiry; refresh-token theft is high impact |
| `sessionStorage` | JavaScript can read tokens after XSS | Similar bearer-header behavior; not a CSRF defense | Usually lost when the tab/window closes; does not provide durable refresh persistence |
| In-memory storage | Tokens are inaccessible to disk and disappear on reload; XSS can still use a live token | Bearer headers are not automatically sent cross-site | Strongest browser-side persistence minimization; requires re-authentication or a secure renewal mechanism after reload |
| `HttpOnly` cookies | JavaScript cannot read the cookie, reducing token-exfiltration impact from XSS; XSS can still send same-origin requests | Cookies are sent automatically, so CSRF protection is required | Supports controlled refresh and persistence with `Secure`, `HttpOnly`, and `SameSite`; lifetime is server-controlled |

The production recommendation is `HttpOnly; Secure; SameSite=Lax` cookies
issued and refreshed by the same-origin backend/BFF, with a CSRF token for every
state-changing request and strict `Origin`/`Referer` validation. The browser
must not receive a refresh token or place auth tokens in web storage. If a
direct browser Supabase client is temporarily used for development, its
configuration must explicitly document whether persistence is enabled; setting
`persistSession: false` is not equivalent to the production cookie design.
Cookie sessions require short access-token lifetimes, refresh-token rotation,
revocation on sign-out, and no cross-site credentialed requests.

### Role provisioning and bootstrap

- Every self-service registration receives exactly `student_user`.
- Reviewer and administrator roles are granted only by a trusted
  administrative workflow after identity verification and, for administrators,
  MFA. The frontend cannot choose a role.
- Signup payloads, user-editable metadata, redirect parameters, and client
  claims are never used as authorization input. Any role-like value from those
  sources is ignored and logged as a rejected escalation attempt.
- The trusted authorization source is a server-controlled role record keyed by
  the verified Supabase subject (`sub`). A server-controlled Supabase custom
  claim may be used as a signed cache only if it is produced by an approved
  server hook; user-editable `user_metadata`, signup JSON, and client claims
  cannot authorize roles because the user can write or replay them.
- Privileged authorization checks the current role record, not only a
  previously issued role claim. A grant, downgrade, or revocation is audited
  with actor, target, previous role, new role, reason, and timestamp; it also
  revokes matching BFF sessions or advances the subject's revocation/version
  marker. Tokens issued before the change are therefore denied on the next
  privileged request rather than remaining authorized until normal JWT
  expiry. If a custom claim is used for performance, its short TTL and
  revocation/version check remain mandatory.
- The first administrator is bootstrapped out-of-band: an operator creates or
  verifies the designated Supabase identity, enables MFA, runs a one-time
  server-side bootstrap operation protected by an injected secret or approved
  deployment control, and confirms the resulting audit record. The bootstrap
  secret is never shipped to the frontend, accepted in a public signup field,
  or left enabled after the first administrator exists. There is no
  self-service "make me admin" feature.

### JWT verification

The backend trusts only the explicitly configured Supabase project issuer and
JWKS endpoint, for example the project-specific Auth JWKS URL. The URL,
issuer, audience, and algorithm are deployment configuration reviewed before
release; arbitrary token-provided URLs are forbidden.

Verification requirements:

- Parse the header only to select a cached key by `kid`; do not authorize from
  any unverified claim.
- Permit only the fixed configured asymmetric algorithm (the deployment must
  choose and document `RS256` or `ES256`; no algorithm substitution, `none`,
  HMAC/asymmetric confusion, or caller-selected algorithm).
- Validate the signature, exact issuer, exact audience (`authenticated` unless
  an approved deployment uses another fixed audience), expiry, and not-before.
- Enforce required subject and role claims only after signature and registered
  claim validation. Missing, malformed, expired, not-yet-valid, or
  wrong-issuer/audience tokens are rejected with an authentication error.
- Cache JWKS keys by `kid` with a bounded TTL and refresh on an unknown `kid`.
  Key rotation is supported by retaining currently valid cached keys while the
  issuer publishes the replacement. If refresh fails, do not accept an
  unknown key: protected requests fail closed with a service-unavailable
  response and public read-only routes may continue only if they do not
  require identity.
- Never fall back to decoding claims without signature verification and never
  silently accept stale or unavailable key material beyond its documented
  validity window.

### Public endpoint policy and limits

NASA research reads and BASS-II reads remain public. Public responses contain
research/dataset information only; they never include reviewer identity,
private review notes, role assignments, audit events, or administrative data.
Expensive operations have separate limits and bounded resource use:

| Endpoint group | Access | Baseline controls |
|---|---|---|
| `GET /health`, `GET /`, `GET /research/search`, `GET /research/online-search`, `GET /research/combined-search`, `GET /research/evidence-search`, `GET /research/nasa-passage-search`, `GET /bass2/search`, `GET /bass2/summary` | Public | Per-IP rate limit; query length 200 characters; `limit` bounded to the documented maximum; response-size cap; no review/admin fields |
| `POST /research/insights` | Public | Separate per-IP rate limit (for example 30/minute); body cap 16 KiB; query length 200; limit cap 20; timeout 10 seconds; concurrent-request cap and cancellation |
| `POST /research/insights/compare` | Public | Stricter separate per-IP rate limit (for example 10/minute); body cap 16 KiB; at most 10 comparison inputs; query/field length caps; timeout 10 seconds; concurrency cap |
| `POST /research/mission-intelligence` | Public research mode only | Stricter separate per-IP rate limit (for example 5/minute); body cap 16 KiB; bounded context fields and limit; timeout 15 seconds; concurrency cap; response excludes reviews and administrative information |
| `POST /research/reviews`, `PATCH /research/reviews/{id}`, review reads/history | Reviewer or administrator only | Verified identity and role; per-user rate limit; CSRF protection; ownership/target authorization; audit logging; no public exposure |
| `POST /research/import/{nasa_id}` | Administrator only | Verified administrator and MFA; separate low rate limit; request/response size caps; upstream timeout; audit event; not in public navigation |

Rate-limit counters must use shared, atomic storage such as the approved
Redis/managed rate-limit service whenever multiple backend workers or
instances can receive traffic. In-memory counters are permitted only for
single-worker development and must not be used to enforce production limits.
Rate-limit keys should combine the verified user subject and client IP when
available, with anonymous requests keyed by client IP.

The trusted proxy configuration is an explicit allowlist of the deployment's
reverse-proxy addresses or networks. Only requests received from that
allowlist may contribute a validated forwarded client IP; direct clients
cannot choose their own rate-limit identity by sending `X-Forwarded-For`.
When no trusted proxy is present, use the immediate socket peer address and
ignore forwarded headers. The proxy must strip incoming forwarding headers
before adding its own, and changes to the allowlist require deployment
review. Abuse controls also include rejecting oversized JSON, excessive
nesting, unknown fields where appropriate, repeated identical expensive
requests, abusive concurrency, and upstream timeouts. Limits are operational
defaults until capacity testing approves exact values; they must not be
removed merely because an endpoint is public.

### Review ownership and append-only revisions

Ownership is derived only from the verified backend subject (`sub`) and never
from `reviewer_id`, `owner_id`, or any other client-supplied field. The review
root has at most one current owner, enforced transactionally by a unique
constraint on the review target (`target_type`, `target_id`) in the ownership
mapping. A separate unique review identifier prevents duplicate roots.
Conflicting create or transfer operations fail explicitly and are audited; they
do not overwrite an existing owner.

Existing reviews are preserved with `owner_user_id = NULL`. NULL means legacy
or unassigned ownership, not ownership by the caller. A trusted reviewer/admin
workflow may assign an owner after verification, but ordinary review updates
cannot claim or change ownership. The immutable review root stores the owner
identity; every append-only revision references that root and records the
verified actor and effective owner snapshot. Ownership transfer, if approved,
is a distinct audited event, so revisions cannot diverge or create duplicate
owners.

### SQLite migration and data-safety decision

The initial development implementation remains on the existing SQLite
database. PostgreSQL is not introduced without a demonstrated technical
blocker, such as a measured concurrency, durability, or deployment requirement
that SQLite cannot satisfy and that is approved separately.

No existing database or dataset may be modified without explicit approval.
Before any approved schema change, the plan requires:

1. A read-only backup and SHA-256 checksum of the source database and relevant
   dataset files.
2. A migration copy created in a separate path; the source remains untouched.
3. Migration-copy tests covering schema, row counts, NULL legacy ownership,
   unique constraints, append-only revisions, and representative endpoint
   reads/writes.
4. Verification of checksums for unchanged source files, expected migrated
   values, foreign keys, indexes, and application smoke tests.
5. A rollback procedure that stops the new process, preserves failed artifacts
   for diagnosis, restores the verified backup/copy, and rechecks its checksum.
   Rollback is not a destructive overwrite and requires explicit operator
   approval.

## 5B. Final security decisions and manual configuration requirements

Final decisions for implementation approval:

- Use the same-origin BFF with Secure HttpOnly cookie sessions in production;
  do not rely on Supabase JS `localStorage` persistence.
- Provision `student_user` on signup only; grant reviewer/admin roles through
  trusted, audited administration, with one-time MFA-protected first-admin
  bootstrap.
- Verify JWTs against one approved issuer/JWKS configuration with one fixed
  asymmetric algorithm and fail closed for protected routes.
- Keep NASA and BASS-II reads public, but rate-limit expensive POST operations
  independently and expose no review/admin data in public responses.
- Enforce one verified owner per review target, preserve NULL legacy ownership,
  and keep ownership consistent through append-only revisions.
- Keep SQLite for initial development; require explicit approval and a tested,
  checksummed copy/rollback process for any migration.

Manual configuration still required before implementation:

- Approve the Supabase project, exact issuer, JWKS URL, audience, fixed
  algorithm, token lifetimes, refresh rotation, cookie domain, and trusted
  origin/CORS policy.
- Configure production HTTPS, Secure/HttpOnly/SameSite cookies, CSRF token
  delivery, proxy-aware client-IP handling, rate-limit storage, request
  timeouts, body/query limits, and observability/alerting.
- Establish the MFA policy, trusted administrator identity, one-time bootstrap
  control, role-change approval/audit retention, and emergency revocation
  procedure.
- Confirm the SQLite file and dataset backup owner, checksum storage,
  migration-copy location, restore test schedule, and rollback approver.
- Approve exact capacity-tested numeric limits and whether public mission
  intelligence remains enabled without review fields.

## 5C. Security testing plan

Tests must be written before implementation approval and must cover:

- Token storage/session behavior: reload, browser restart, sign-out,
  refresh-token rotation, expired sessions, XSS cannot read HttpOnly cookies,
  CSRF rejection, and trusted-origin acceptance.
- JWT negatives: bad signature, unknown `kid`, wrong issuer/audience,
  disallowed algorithm, missing/expired/not-before claims, JWKS outage,
  rotation from old to new key, and refusal to authorize from unverified
  claims.
- Role escalation: signup with `reviewer`/`administrator` fields or metadata,
  forged role claims, direct role endpoints, and first-admin bootstrap replay;
  all must fail and produce the expected audit event.
- Endpoint authorization: public NASA/BASS-II reads work; expensive endpoints
  enforce independent rate/resource limits; review/import operations reject
  anonymous, student, and wrong-owner callers; public responses contain no
  review/admin information.
- Ownership: duplicate target creation, conflicting assignment, client
  owner substitution, concurrent assignment, NULL legacy review access, and
  append-only revision consistency.
- Data safety: backup checksum verification, migration-copy parity, constraint
  checks, rollback rehearsal, and proof that the original SQLite database and
  datasets remain unchanged.

## 6. TypeScript data contracts

The following interfaces model fields observed in the backend. Fields that
vary by source or upstream NASA response are optional or represented as
`unknown`; the frontend must not invent values for them.

```ts
export type JsonPrimitive = string | number | boolean | null;
export type JsonValue =
  | JsonPrimitive
  | JsonValue[]
  | { [key: string]: JsonValue };

export type ApiErrorDetail =
  | string
  | {
      type?: string;
      loc?: Array<string | number>;
      msg?: string;
      input?: unknown;
      [key: string]: unknown;
    }[];
  | Record<string, unknown>;

export interface ApiError {
  detail?: ApiErrorDetail;
}

export interface HealthResponse {
  status: string;
  service: string;
}

export interface ApiIdentityResponse {
  message: string;
  project: string;
  version: string;
}

export interface RankingContract {
  [key: string]: unknown;
}

export interface Provenance {
  source_document_id?: string | number | null;
  document_id?: string | number | null;
  nasa_id?: string | number | null;
  source_url?: string | null;
  citation_url?: string | null;
  page_numbers?: number[];
  sections?: string[];
  review_status?: string | null;
  [key: string]: unknown;
}

export interface SupportingEvidence {
  source_document_id?: string | number | null;
  nasa_id?: string | number | null;
  source_url?: string | null;
  page_numbers?: number[];
  section_name?: string | null;
  evidence_type?: string | null;
  exact_supporting_text?: string | null;
  exact_supporting_excerpt?: string | null;
  extraction_method?: string | null;
  verification_status?: string | null;
  uncertain?: boolean;
  [key: string]: unknown;
}

export interface Claim {
  claim_id?: string | null;
  claim_text?: string | null;
  claim_type?: string | null;
  source_document_id?: string | number | null;
  nasa_id?: string | number | null;
  source_url?: string | null;
  source_title?: string | null;
  exact_supporting_excerpt?: string | null;
  exact_supporting_text?: string | null;
  page_numbers?: number[];
  section_name?: string | null;
  evidence_type?: string | null;
  verification_status?: string | null;
  uncertain?: boolean;
  supporting_evidence?: SupportingEvidence[];
  scientific_findings_verified?: boolean;
  [key: string]: unknown;
}

export interface StructuredFindingValue {
  field?: string | null;
  value?: string | null;
  raw_value?: string | null;
  unit?: string | null;
  exact_supporting_text?: string | null;
  source_document_id?: string | number | null;
  nasa_id?: string | number | null;
  source_url?: string | null;
  page_numbers?: number[];
  section_name?: string | null;
  evidence_type?: string | null;
  extraction_method?: string | null;
  verification_status?: string | null;
  uncertain?: boolean;
  [key: string]: unknown;
}

export interface StructuredFindings {
  schema_version?: string;
  source?: Provenance;
  fields?: Record<
    string,
    { status?: string; values?: StructuredFindingValue[] }
  >;
  evidence?: StructuredFindingValue[];
  observations?: StructuredFindingValue[];
  findings?: StructuredFindingValue[];
  limitations?: StructuredFindingValue[];
  uncertainty_notes?: Array<Record<string, unknown>>;
  [key: string]: unknown;
}

export interface ResearchPaper {
  document_id?: string | number | null;
  nasa_id?: string | number | null;
  source_url?: string | null;
  source_title?: string | null;
  source_type?: string | null;
  evidence_classification?: string | null;
  verification_status?: string | null;
  review_status?: string | null;
  scientific_findings_verified?: boolean;
  summary?: Record<string, unknown>;
  claims?: Claim[];
  structured_findings?: StructuredFindings;
  provenance?: Provenance;
  [key: string]: unknown;
}

export interface RetrievalSummary {
  strategy?: string;
  fallback_triggered?: boolean;
  fallback_reason?: string[] | string | null;
  missing_query_concepts?: string[];
  online_search?: Record<string, unknown>;
  counts?: Record<string, number>;
  [key: string]: unknown;
}

export interface EvidenceCollection {
  paper_count?: number;
  claim_count?: number;
  papers?: ResearchPaper[];
  claims?: Claim[];
  [key: string]: unknown;
}

export interface ResearchInsightsResponse {
  schema_version?: string;
  query: string;
  retrieval?: RetrievalSummary;
  evidence?: EvidenceCollection;
  conflict_report?: Record<string, unknown>;
  recommendation?: string;
  scientific_findings_verified?: boolean;
  notices?: string[];
  limitations?: string[];
  [key: string]: unknown;
}
```

### NASA catalogue contracts

```ts
export interface NASARecord {
  title?: string | null;
  abstract?: string | null;
  nasa_id?: string | number | null;
  source_url?: string | null;
  source?: string | null;
  authors?: Array<{ name?: string | null; affiliation?: string | null }>;
  publication_date?: string | null;
  keywords?: string[];
  subject_categories?: string[];
  document_type?: unknown;
  dissemination_status?: unknown;
  document_available?: boolean;
  center?: string | null;
  verification_status?: string | null;
  evidence_type?: string | null;
  full_text_retrieved?: boolean;
  scientific_findings_verified?: boolean;
  review_status?: string | null;
  relevance_score?: number;
  matching_reasons?: string[];
  retrieval_timestamp?: string;
  retrieved_at?: string;
  ranking_contract?: RankingContract;
  [key: string]: unknown;
}

export interface NASAOnlineSearchResponse {
  source?: string;
  query: string;
  normalized_query?: string;
  count: number;
  results: NASARecord[];
  retrieval_timestamp?: string;
  retrieved_at?: string;
  original_query?: string;
  nasa_query?: string;
  fallback_attempted?: boolean;
  fallback_reason?: string | null;
  original_result_count?: number;
  fallback_result_count?: number;
  fallback_attempts?: Array<Record<string, unknown>>;
  error?: string;
  [key: string]: unknown;
}

export interface NASAPassage {
  nasa_id?: string | null;
  source_type?: string;
  title?: string | null;
  pdf_page_number?: number | null;
  citation_url?: string | null;
  source_field?: string | null;
  snippet?: string | null;
  matched_terms?: string[];
  relevance_score?: number;
  exact_phrase_match?: boolean;
  classification?: string | null;
  classification_status?: string | null;
  classification_basis?: string | null;
  evidence_type?: string | null;
  research_status?: string | null;
  experimental_result_status?: string | null;
  review_status?: string | null;
  scientific_findings_verified?: boolean;
  relevance_components?: Record<string, unknown>;
  matching_reasons?: string[];
  ranking_contract?: RankingContract;
  [key: string]: unknown;
}

export interface NASAPassageSearchResponse {
  query: string;
  filters: { nasa_id?: string | null; classification?: string | null };
  count: number;
  results: NASAPassage[];
  notice: string;
}

export interface ReviewedEvidence {
  evidence_id?: string | null;
  nasa_id?: string | number | null;
  title?: string | null;
  finding?: string | null;
  evidence_class?: string | null;
  pdf_page_number?: number | null;
  citation_url?: string | null;
  review_status?: string | null;
  scientific_findings_verified?: boolean;
  matched_terms?: string[];
  relevance_score?: number;
  source_type?: string;
  ranking_contract?: RankingContract;
  [key: string]: unknown;
}

export interface ReviewedEvidenceSearchResponse {
  query: string;
  count: number;
  results: ReviewedEvidence[];
  notice: string;
}
```

### Comparison, mission, BASS-II, and review contracts

```ts
export interface ConditionComparison {
  dimension?: string;
  status?: string;
  first_source_values?: StructuredFindingValue[];
  second_source_values?: StructuredFindingValue[];
  missing_information?: string[];
  [key: string]: unknown;
}

export interface ComparisonResponse {
  schema_version?: string;
  query: string;
  retrieval?: RetrievalSummary;
  evidence?: EvidenceCollection;
  comparison?: {
    sources?: Array<Record<string, unknown>>;
    comparable_sources?: Array<Record<string, unknown>>;
    non_comparable_sources?: Array<Record<string, unknown>>;
    condition_comparisons?: ConditionComparison[];
    comparison_limitations?: string[];
    scientific_findings_verified?: boolean;
    [key: string]: unknown;
  };
  conflicts?: Array<Record<string, unknown>>;
  research_gaps?: Array<Record<string, unknown>>;
  suggested_research_questions?: Array<Record<string, unknown>>;
  comparison_limitations?: string[];
  recommendation?: string;
  scientific_findings_verified?: boolean;
  [key: string]: unknown;
}

export interface Bass2Record {
  PI?: string;
  "Test #"?: string;
  Date?: string;
  GMT?: string;
  "Sample #"?: string;
  "Fuel Sample Material"?: string;
  "Flow restrictor"?: string;
  "Fan display"?: string;
  "Air display"?: string;
  "Radiometer gain   (1000   250   50   10)"?: string;
  "Total Frames Shot"?: string;
  "Calibrated  initial O2 % by vol "?: string;
  "Calibrated final O2 % by vol"?: string;
  "Initial CO2 % by vol"?: string;
  "Final CO2 % by vol"?: string;
  "Initial CO (ppm)"?: string;
  "Final CO (ppm)"?: string;
  [key: string]: string | undefined;
}

export interface Bass2SearchResult {
  record: Bass2Record;
  source_type: "bass_ii";
  matched_terms?: string[];
  relevance_score?: number;
  relevance_components?: Record<string, unknown>;
  matching_reasons?: string[];
  ranking_contract?: RankingContract;
}

export interface Bass2SummaryResponse {
  dataset_name?: string | null;
  record_count?: number;
  declared_record_count?: number;
  column_count?: number;
  pi_counts?: Record<string, number>;
  blank_cells?: number;
  literal_none_cells?: number;
  duplicate_identifiers?: Array<{ PI?: string; "Test #"?: string }>;
  quality_flags_count?: number;
  source_values_modified?: boolean;
  scientific_findings_verified?: boolean;
}

export interface Bass2SearchResponse {
  query: string;
  filters: Record<string, string | number | null>;
  count: number;
  results: Bass2SearchResult[];
  notice: string;
}

export type ReviewStatus =
  | "pending"
  | "accepted"
  | "rejected"
  | "needs_correction"
  | "insufficient_evidence";

export type ReviewTargetType =
  | "paper"
  | "claim"
  | "structured_finding"
  | "comparison"
  | "conflict"
  | "research_gap"
  | "mission_brief";

export interface ReviewRecord {
  review_id: string;
  revision: number;
  target_type: ReviewTargetType;
  target_id: string;
  source_document_id?: string | null;
  nasa_id?: string | null;
  source_url?: string | null;
  reviewer_id?: string | null;
  reviewer_identity_status?: string;
  status: ReviewStatus;
  reviewer_decision?: string | null;
  reviewer_notes?: string | null;
  correction_notes?: string | null;
  scientific_findings_verified?: boolean;
  evidence_scope?: string | null;
  created_at?: string;
  updated_at?: string;
}

export interface ReviewListResponse {
  count: number;
  reviews: ReviewRecord[];
}

export interface ReviewHistoryResponse {
  review_id: string;
  history: ReviewRecord[];
}

export interface MissionIntelligenceResponse
  extends ResearchInsightsResponse {
  mission_context?: Record<string, unknown>;
  comparison?: ComparisonResponse["comparison"];
  conflicts?: Array<Record<string, unknown>>;
  research_gaps?: Array<Record<string, unknown>>;
  suggested_research_questions?: Array<Record<string, unknown>>;
  bass2_evidence?: Record<string, unknown>;
  reviews?: {
    records?: ReviewRecord[];
    accepted_review_present?: boolean;
    authentication_status?: string;
  };
  mission_research_brief?: Record<string, unknown>;
  conclusion?: string;
}
```

The `GET /dashboard/mission-brief` response is a separate legacy contract and
should initially be represented as `Record<string, unknown>` behind a
compatibility adapter until its complete response is needed by the UI. The
frontend must not treat it as interchangeable with
`MissionIntelligenceResponse`.

## 7. API client design

### Client responsibilities

`api/client.ts` should:

- Accept a configurable base URL; do not hardcode a production URL because
  none is defined.
- Serialize query parameters without changing field names or whitespace
  significant BASS-II column names.
- Send JSON for POST/PATCH bodies.
- Parse JSON error bodies, including object-valued `detail`.
- Preserve HTTP status codes.
- Support `AbortSignal`.
- Never send `db_path`.
- Never expose server filesystem paths as user-editable values.

### Feature request state

Each screen should model:

```ts
type RequestState<T> =
  | { status: "idle"; data: null; error: null }
  | { status: "loading"; data: T | null; error: null }
  | { status: "success"; data: T; error: null }
  | { status: "empty"; data: T; error: null }
  | { status: "error"; data: T | null; error: ApiError };
```

`empty` is a UI interpretation of a successful response with zero records,
not a backend response status.

## 8. Screen plans

### Overview

- Call `GET /health` on load.
- Display service status only; do not imply dataset/scientific validation.
- Link to research, NASA, BASS-II, comparison, mission intelligence, and
  review workflows.
- Show persistent disclaimer:
  "Research support only. Retrieved evidence is not automatically scientifically
  verified or a certified fire-safety limit."

### Research Search

- Form: `q`, `limit`.
- Primary call: `POST /research/insights`.
- Optional advanced local call: `GET /research/search`.
- Result cards show paper, claims, exact excerpt, page/section provenance,
  source URL, verification/review status, and limitations.
- Show NASA fallback status from `retrieval.online_search`.
- Show `InsufficientEvidenceState` when recommendation is the backend's
  insufficient-evidence message or verified evidence is false.

### NASA Catalogue

Tabs or sections:

1. Online metadata: `GET /research/online-search`.
2. Extracted passages: `GET /research/nasa-passage-search`.
3. Reviewed evidence: `GET /research/evidence-search`.

Clearly distinguish metadata, extracted passages, and reviewed records.
Import is an explicit privileged action using
`POST /research/import/{nasa_id}` only after product/security approval.

### BASS-II Dataset

- Load summary from `GET /bass2/summary`.
- Search records with `GET /bass2/search`.
- Preserve original strings in the record drawer/table.
- Use exact supported numeric field names only.
- Do not add UI filters for gravity, pressure, temperature, spread rate, or
  extinction outcome; those fields are unavailable.
- Show the dataset's `scientific_findings_verified: false` state.

### Compare & Gaps

- Submit `POST /research/insights/compare`.
- Render condition comparison statuses, missing information, conflicts,
  research gaps, and suggested questions.
- Explain that `mismatch` means non-comparable reported conditions, not a
  verified scientific contradiction.
- Display `independence_status: unknown` when supplied.

### Mission Intelligence

- Collect only supported mission context values.
- Submit `POST /research/mission-intelligence`.
- Render mission brief applicability classifications:
  `exact_match`, `partial_match`, `different_conditions`, and
  `unknown_conditions`.
- Keep BASS-II context separate from NASA paper evidence.
- Show reviews as workflow state, not scientific certification.
- Do not show operational fire-safety instructions because the backend does not
  provide them.

### Human Review

- List with `GET /research/reviews`.
- Inspect current record with `GET /research/reviews/:reviewId`.
- Inspect revisions with `GET /research/reviews/:reviewId/history`.
- Create via `POST /research/reviews`.
- Update via `PATCH /research/reviews/:reviewId`.
- Display unauthenticated identity warning next to reviewer fields.
- Never label `accepted` as scientifically verified.

## 9. Design system proposal

### Visual direction

Use a restrained scientific operations interface:

- Dark charcoal/navy application shell.
- High-contrast off-white content surfaces.
- Amber/orange reserved for warnings and review-required states.
- Blue for links and source navigation.
- Green only for service/process health, not scientific validity.
- Red reserved for request failures or explicit high-risk warnings.

Avoid visual treatments that imply certainty, such as confidence gauges,
probability meters, or green "validated" badges when the backend reports
`scientific_findings_verified: false`.

### Tokens

Define CSS variables for:

- Background, surface, elevated surface, border, text, muted text.
- Brand, info, warning, danger, success.
- Spacing scale.
- Border radius.
- Typography sizes and line heights.
- Focus ring and minimum touch target.

### Responsive layout

#### Desktop, 1200px and above

- Persistent left navigation.
- Two-column research layout: filters/results and provenance/detail panel.
- Comparison matrix and BASS-II table use full width.
- Mission screen can show context, evidence, and review panels in columns.

#### Tablet, 768px-1199px

- Collapsible navigation rail.
- Single main content column with optional side panels below.
- Comparison matrix allows horizontal scrolling with sticky source labels.
- BASS-II table uses horizontal scroll and column visibility controls.

#### Mobile, below 768px

- Top navigation with menu drawer.
- Single-column cards.
- Provenance and limitations become expandable sections but remain available.
- Tables become stacked record cards or horizontal scroll regions.
- Query controls stack vertically.
- Do not hide verification labels or source URLs behind inaccessible hover
  interactions.

### Accessibility

- Keyboard-accessible navigation, dialogs, tables, and accordions.
- Visible focus states.
- Semantic headings and landmarks.
- `aria-live` announcements for request completion/errors.
- Color is never the only verification or status signal.
- Long excerpts remain selectable and readable at increased text size.

## 10. Loading, error, empty, and insufficient-evidence states

### Loading

- Show skeletons for cards/tables.
- Preserve the previous successful data during refresh where useful.
- Provide cancellation for NASA-backed requests.
- Explain that NASA catalogue calls may be slow.

### Error

| HTTP status | Frontend behavior |
|---:|---|
| 400 | Show actionable validation message near the form |
| 404 | Show missing-record state with navigation back |
| 422 | Render field-level FastAPI validation details |
| 502 | Explain NASA/import upstream failure and offer retry |
| 503 | Explain unavailable local data/service dependency and offer retry |
| Network/timeout | Explain backend connectivity or CORS/deployment issue |

Do not convert errors into empty successful results.

### Empty

Differentiate:

- No query/filter supplied.
- Valid query with zero local matches.
- Valid search with zero NASA catalogue matches.
- No BASS-II records matched.
- No review records.
- No history for a valid review.

### Insufficient evidence

Use a distinct non-error state when:

- `scientific_findings_verified` is false.
- The recommendation is the backend insufficient-evidence message.
- Comparison fields are unknown or partial.
- Mission conditions do not exactly match retrieved studies.

The state should display the backend explanation and limitations, not invent a
numeric confidence score.

## 11. Implementation sequence

### Phase 0: decisions and blockers

1. Approve frontend framework and repository location.
2. Confirm development and production backend base URLs.
3. Decide deployment topology so CORS is either configured or avoided through
   same-origin serving.
4. Define whether review endpoints are available to the first frontend
   release.
5. Decide whether NASA import is excluded from the public product.

### Phase 1: foundation

1. Scaffold the selected TypeScript frontend without changing backend files.
2. Add app shell, responsive navigation, route placeholders, design tokens,
   accessibility baseline, and error boundary.
3. Add typed API client and request-state utilities.
4. Add reusable provenance, verification, limitations, loading, error, and
   empty-state components.

### Phase 2: read-only research workflows

1. Implement Overview and health status.
2. Implement Research Search with `/research/insights`.
3. Implement NASA Catalogue search tabs.
4. Implement BASS-II summary/search.
5. Add responsive and accessibility validation.

### Phase 3: analysis workflows

1. Implement comparison and gap analysis.
2. Implement mission intelligence.
3. Add ranking explanations and condition applicability views.
4. Add contract fixtures based on observed response shapes.

### Phase 4: human review

1. Implement review list/detail/history.
2. Implement create/update only after authentication and authorization policy
   is approved.
3. Display reviewer identity limitations.

### Phase 5: release hardening

1. Add backend integration tests against a configured environment.
2. Test network timeout, NASA upstream failure, 400/404/422/502/503 responses,
   and malformed/additive response fields.
3. Validate CORS/deployment behavior.
4. Run accessibility, keyboard, mobile, and visual regression checks.
5. Review every scientific label and recommendation for provenance fidelity.

## 12. Identified blockers and risks

### Blocking product/infrastructure decisions

- No existing frontend framework or package manifest.
- No approved frontend deployment target.
- Production backend URL is unverified.
- No CORS configuration.
- No authentication or authorization.
- Human review identity is unauthenticated.
- Review tenancy and access control are undefined.

### Backend contract risks

- Several request bodies are untyped dictionaries.
- Some response shapes are source-dependent and have optional fields.
- NASA upstream failures can return HTTP 200 with an `error` field.
- `/research/import/{nasa_id}` mutates persistent data.
- Legacy `/dashboard/mission-brief` is a separate contract.
- No generated, versioned TypeScript/OpenAPI client is available.

### Scientific UX risks

- Lexical relevance scores can be mistaken for confidence.
- Accepted review status can be mistaken for scientific certification.
- NASA abstracts can be mistaken for full-text evidence.
- BASS-II metadata can be mistaken for flame-spread outcomes.
- Missing conditions can be mistaken for negative findings.
- Comparison mismatches can be mistaken for scientific contradictions.

## 13. Phase 1 acceptance criteria

Before frontend implementation is considered ready to begin:

- Framework and frontend location are approved.
- Backend base URL and CORS/deployment strategy are known.
- The typed interfaces and endpoint mapping in this plan are reviewed.
- Product owners approve the visible verification and limitation language.
- Public versus privileged access to review and import endpoints is decided.
- The first release scope is limited to capabilities actually exposed by the
  backend.

## Final recommendation

Proceed with a read-only research dashboard first, centered on
`/research/insights`, NASA search, BASS-II browsing, comparison/gap analysis,
and mission intelligence. Defer authenticated review administration and NASA
document import until identity, authorization, CORS, and deployment policies
are resolved. This approach supports frontend development without presenting
unverified evidence as scientific certification or inventing unavailable
backend capabilities.
