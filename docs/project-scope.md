# Project Scope: AI Code Assistant

This document enumerates goals, phases, functional scope, architectural direction, constraints, risks, and success metrics. It complements `.github/copilot-instructions.md`.

---

## 1. Vision

Provide a developer-facing AI assistant that:

- Explains arbitrary code snippets in plain language.
- Suggests refactors for readability/maintainability.
- Generates unit test scaffolds (Pytest / Jest patterns).
- Evolves into a conversational assistant that can automatically choose specialized tooling (MCP style).
- Eventually supports history, authentication, cost awareness, and optional repository/file retrieval.

---

## 2. In-Scope (Initial to Mid Phases)

| Capability                                     | Phase     | Description                                                                    |
| ---------------------------------------------- | --------- | ------------------------------------------------------------------------------ |
| Basic FastAPI + React pipeline                 | 1         | Health check + placeholder explain endpoint                                    |
| OpenAI integration (explain)                   | 2         | Real LLM explanation output                                                    |
| Additional endpoints: refactor, generate tests | 3         | Structured outputs, consistent DTO design                                      |
| Shared schema -> TS codegen                    | 4 (start) | Backend source-of-truth Pydantic models exported to frontend                   |
| Chat-like interface (manual dispatch)          | 4         | Natural language triggers correct endpoint                                     |
| Tool registry design (MCP-ready)               | 4-5       | Abstracted mapping: intent → command                                           |
| MCP integration (internal)                     | 5         | Provide tool schema definitions; potential external orchestrator compatibility |
| Observability basics                           | 5-6       | Structured logging, request correlation (foundation)                           |
| Persistence (history)                          | 6         | PostgreSQL store for past interactions                                         |
| Authentication (JWT)                           | 6-7       | Basic user accounts (optional at this stage)                                   |
| Cost tracking (LLM usage metrics)              | 6-7       | Logging tokens or cost per call, aggregated summary                            |

---

## 3. Out of Scope (Early Phases)

- Multi-tenant billing.
- Full RBAC system.
- Fine-tuned LLM models.
- Large-scale distributed architecture or microservices.
- Real-time collaborative code editing.
- RAG/document retrieval (may appear in future extension phase).
- Complex queue-based background processing (unless needed later).
- Streaming output (initial phases may return full responses only).

---

## 4. Phased Plan (Detailed)

### Phase 1 – Foundations

- Backend: FastAPI skeleton; `/ping`; `/api/v1/explain` placeholder.
- Application: `ExplainCodeCommand` + handler + dispatcher; `AIProvider` abstraction with `FakeAIProvider`.
- Frontend: React + Vite + Monaco editor; call explain endpoint; show JSON.
- Deliverable: End-to-end vertical slice (placeholder explanation).
- Exit Criteria: Command architecture proven; test passes.

### Phase 2 – Real AI (Explain)

- Add OpenAI provider implementation.
- Configuration via Pydantic settings; fallback to Fake when key missing.
- Basic error mapping for provider failures.
- Prompt design (initial simple system prompt).
- Tests: Handler with mocked provider; integration test covering provider fallback.
- Exit Criteria: Real explanation functioning with environment key.

### Phase 3 – Multi-Functionality

- Add `RefactorCodeCommand`, `GenerateTestsCommand` + handlers.
- Extend `AIProvider` with `refactor()` and `generate_tests()`.
- Add endpoints: `/api/v1/refactor`, `/api/v1/tests`.
- Standardize response metadata: `provider`, `version`, `processing_time_ms`.
- Frontend: Buttons for each action; syntax highlighting of returned code blocks.
- Exit Criteria: Three stable endpoints, shared response schema pattern.

### Phase 4 – Shared Schemas + Early Chat

- Introduce codegen script (Pydantic JSON Schema → TS interfaces).
- Chat UI component that allows natural language selection (front-end logic maps keywords to endpoints initially).
- Begin tool abstraction: `ToolDescriptor` (name, description, input_schema, output_schema).
- Exit Criteria: Frontend consumes generated TS types; basic chat works.

### Phase 5 – MCP / Tool-Oriented Assistant

- Formalize internal `ToolRegistry` referencing available commands.
- Provide tool schema JSON (future external agent compatibility).
- Chat backend endpoint decides tool selection either via classification or LLM function calling.
- Exit Criteria: Natural language request triggers correct tool automatically without direct buttons.

### Phase 6 – Persistence & Observability

- Add PostgreSQL + SQLAlchemy/SQLModel.
- Repositories + unit-of-work pattern (optional if complexity merits).
- Store snippet, action type, result metadata & timestamp.
- Add structured logging & correlation ID middleware.
- Token usage logging if available from provider.
- Exit Criteria: History UI listing past interactions; logs contain structured fields.

### Phase 7 – Authentication & Cost Tracking

- User registration/login (JWT).
- Per-user history filtering.
- Basic cost summary endpoint (aggregate approximate token usage).
- Exit Criteria: Auth-protected history; cost displayed.

### Future Extensions (Phase 8+)

- Streaming token responses.
- RAG: Embedding repository docs for context augmentation.
- Multi-language test generation strategy adaptors.
- Plugin architecture for additional “tools” (e.g., complexity analysis).

---

## 5. Architectural Tenets

1. Keep domain small & explicit.
2. All AI provider logic behind `AIProvider` interface (single responsibility).
3. Commands are immutable; handlers are stateless except injected dependencies.
4. Presentation only maps HTTP <-> DTO; no business logic.
5. Expansion via new commands rather than conditionals in handlers.

---

## 6. Technology Choices & Rationale

| Area              | Choice                        | Reason                                                       |
| ----------------- | ----------------------------- | ------------------------------------------------------------ |
| Backend Framework | FastAPI                       | Async, type hints, ecosystem maturity                        |
| LLM Provider      | OpenAI (initial)              | Availability, stable API, cost-effective model (gpt-4o-mini) |
| Data Layer        | Deferred; SQLAlchemy/SQLModel | Avoid early complexity; widely adopted                       |
| Configuration     | Pydantic settings             | Type-safe, environment variable mapping                      |
| Frontend Build    | Vite                          | Fast dev, ESM                                                |
| Editor            | Monaco                        | Rich language support                                        |
| Styling           | Minimal (initial)             | Focus on functionality first; later theming                  |
| Codegen           | JSON Schema → TS              | Single source-of-truth for contracts                         |

---

## 7. Data & Model Contracts (Early)

Explain Response (initial shape):

```
{
  "explanation": string,
  "line_count": number,
  "char_count": number,
  "provider": string,
  "placeholder": boolean
}
```

Refactor & Test Generation will add:

```
{
  "type": "refactor" | "tests",
  "content": string (code or test suggestions),
  "notes": string (optional),
  "provider": string,
  "processing_time_ms": number
}
```

(Exact details to be finalized in Phase 3; Copilot should update schema + codegen consistently.)

---

## 8. Non-Functional Requirements

| Aspect          | Requirement (Initial)                           |
| --------------- | ----------------------------------------------- |
| Latency         | < 2s typical for short snippets (non-streaming) |
| Availability    | Dev environment only; no formal SLO yet         |
| Observability   | Basic structured logs Phase 5–6                 |
| Security        | Secret isolation, minimal surface area early    |
| Scalability     | Not prioritized until persistence & auth        |
| Maintainability | Clear layering, test coverage for handlers      |

---

## 9. Risks & Mitigations

| Risk                               | Impact               | Mitigation                                      |
| ---------------------------------- | -------------------- | ----------------------------------------------- |
| Scope creep (adding RAG early)     | Delays core features | Enforce phase discipline                        |
| Tight coupling to OpenAI specifics | Harder multi-vendor  | Keep provider interface narrow                  |
| Premature DB schema                | Rework               | Defer persistence until Phase 6                 |
| Unstable prompt outputs            | Flaky tests          | Focus on structural tests & tolerant assertions |
| Token cost overruns                | Expense              | Logging cost metrics; environment gating        |

---

## 10. Success Metrics (Incremental)

| Phase | Metrics                                                           |
| ----- | ----------------------------------------------------------------- |
| 2     | >90% of test snippets produce coherent explanation                |
| 3     | Refactor/test suggestions accepted by user 50%+ (qualitative)     |
| 4     | Zero manual endpoint selection needed in 70% of chat interactions |
| 6     | History retrieval under 200ms for typical user                    |
| 7     | Auth flow + cost summary functional                               |

---

## 11. Testing Evolution

- Phase 1–2: Unit tests (handlers) + integration test per endpoint.
- Phase 3–4: Expand to covering multiple action flows; snapshot diff tests for refactored code (light tolerance).
- Phase 6+: Add database integration tests with isolated test schema / transactional rollback.
- Future: Contract tests for tool schemas (schema drift detection).

---

## 12. Deployment Strategy (Preview)

- Local: `docker-compose` (backend, frontend, db when added).
- Remote (initial):
  - Backend: Fly.io / Render.
  - Frontend: Vercel / Netlify (static build).
  - Shared env secrets (OpenAI API key).
- Add GitHub Actions pipeline once basic multi-endpoint functionality stable.

---

## 13. Observability Plan (Later Phases)

- Middleware: request ID injection.
- Log events: `ai_call_start`, `ai_call_success`, `ai_call_failure`.
- Cost metrics aggregated daily (Phase 6–7).
- Optional: simple `/metrics` (Prometheus) if needed.

---

## 14. Extension Ideas (Ideation Backlog)

| Idea                             | Rationale                         |
| -------------------------------- | --------------------------------- |
| Language autodetect              | Improve prompt specialization     |
| Complexity estimation            | Offer maintainability suggestions |
| Security scan (basic heuristics) | Identify unsafe patterns          |
| Diff-based refactor              | Only emit changed hunks           |
| Multi-file context               | Provide repository-level analysis |
| Streaming partial explanations   | Better UX for long processing     |

(Backlog items require ADR if architectural impact.)

---

## 15. Change Management

- New architectural direction → ADR.
- Schema changes → update Python DTO + regenerate TS + note in CHANGELOG (when introduced).
- Breaking changes across layers → bump minor version (internal tagging policy).

---

## 16. Open Questions (To Track)

1. Will refactor output always be full code or patch/diff format?
2. Should test generation differentiate frameworks (Pytest vs unittest) automatically?
3. Token usage API reliability for cost tracking?
4. How to manage multi-language syntax highlighting gracefully (Monaco config dynamic loading)?
5. Are we adopting streaming before or after persistence?

(Resolve individually; each may spawn ADR.)

---

## 17. Immediate Next Steps (From Initial Commit Point)

1. Implement OpenAI provider (Phase 2).
2. Add exception mapping & logging foundation.
3. Add refactor & test commands (Phase 3 scaffolds).
4. Introduce schema export & TS codegen.
5. Define tool registry draft (Phase 4 start).

---

## 18. Glossary (See also copilot-instructions)

- Vertical Slice: Narrow end-to-end feature implementation.
- Tool Schema: JSON description of function (name, input, output) for LLM tool calling or MCP.
- DTO: Serialized boundary object for request/response.

---

## 19. Document Maintenance

- Update this file upon phase completion (append Phase Status section).
- Add a "Changelog" section when first stable release tag is created.
- Close open questions with references to ADRs.

---

## 20. Phase Status Tracker (Initialize)

| Phase | Status                             | Notes |
| ----- | ---------------------------------- | ----- |
| 1     | Completed (scaffold + placeholder) |       |
| 2     | Not started                        |       |
| 3     | Not started                        |       |
| 4     | Not started                        |       |
| 5     | Not started                        |       |
| 6     | Not started                        |       |
| 7     | Not started                        |       |

(Keep updated manually.)

---

End of project scope.
