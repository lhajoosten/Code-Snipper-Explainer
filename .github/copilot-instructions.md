# GitHub Copilot Project Instructions

These instructions tell GitHub Copilot (and any AI assistant) how to collaborate on this repository.  
They reflect: developer background (transitioning from .NET/Angular/SQL Server to Python/FastAPI + React/TypeScript + PostgreSQL + AI tooling), Clean Architecture, DDD, CQRS, testability, and a phased AI feature roadmap.  
Complementary reference: `docs/project-scope.md`

---

## 1. Developer & Context

- Prior expertise: C#, SOLID, DDD, Clean Architecture, CQRS (MediatR), Repository, Specification, DI, Event-driven patterns, EF Core, Identity, AutoMapper, layered architectures.
- Current stack goal: Python (FastAPI, SQLAlchemy/SQLModel), React + TypeScript, PostgreSQL, LLM/AI integration (OpenAI initially), MCP (Model Context Protocol) for tool orchestration.
- Emphasis: Maintainability, readability, clear separation of concerns, testability (unit + integration), explicit architecture decisions (ADRs), incremental vertical slices.

---

## 2. Project Summary

An “AI Code Assistant” that:

1. Explains arbitrary code snippets.
2. Suggests refactors.
3. Generates unit test scaffolds.
4. Evolves into a chat + tool orchestration assistant (MCP-style tool selection).
5. Later: history persistence, authentication, cost logging, deployment (Docker), possible RAG expansions.

Phased evolution is documented in `docs/project-scope.md`. Copilot must **respect the current phase** and avoid prematurely adding complexity (e.g., database migrations before persistence phase).

---

## 3. Architectural Principles

1. Clean Architecture layering:
   - Domain: Core concepts (Entities, Value Objects, Domain Services) — framework-agnostic.
   - Application: Use cases (Commands/Queries + Handlers), DTOs, orchestration & interfaces (ports).
   - Infrastructure: External implementations (AI providers, persistence adapters, messaging, etc.).
   - Presentation: FastAPI routers, dependency wiring, input/output models.
2. Dependency direction: `presentation -> application -> domain`; `infrastructure` implements interfaces declared in application/domain.
3. CQRS style: Separate command/query handlers; mediator-like dispatcher (custom minimal) unless complexity justifies a library.
4. Explicit interfaces / protocols for pluggability and testability.
5. Immutable value objects where feasible (frozen dataclasses / Pydantic models).
6. Small cohesive modules; single responsibility.
7. Avoid leaking infrastructure concerns upward (e.g., raw OpenAI client objects in handlers).
8. Progressive enhancement: Start simple, iterate vertically.

---

## 4. Directory Structure (Initial Monorepo)

```
/backend
  /app
    /domain
    /application
      /commands
      /queries  (added when needed)
      /handlers
      /dto
      /interfaces
      dispatch.py
    /infrastructure
      /ai
      /persistence (future)
    /presentation
      /api/v1
      dependencies.py
      startup.py
    main.py
  /tests
    (mirrors application + presentation for unit tests)
/frontend
  /src
    /components
    /pages
    /hooks
    /services   (API clients, adapters)
    /types
    /state      (if using Zustand/Redux later)
    /utils
/docs
  project-scope.md
  /architecture
    overview.md
    adr-XXXX-*.md
.github
  copilot-instructions.md
```

---

## 5. Layer Responsibilities (Copilot Must Adhere)

| Layer          | Allowed Dependencies                | Forbidden Practices                                  |
| -------------- | ----------------------------------- | ---------------------------------------------------- |
| Domain         | Python stdlib only (ideally)        | Importing FastAPI, database sessions, OpenAI SDK     |
| Application    | Domain + internal application types | Concrete infrastructure implementations              |
| Infrastructure | Application interfaces              | Importing presentation routers                       |
| Presentation   | Application DTOs/interfaces         | Embedding domain logic; direct use of raw AI clients |

---

## 6. Pattern Translation (.NET → Python/React)

| .NET Concept      | Python Equivalent                                                      |
| ----------------- | ---------------------------------------------------------------------- |
| MediatR           | Custom dispatcher (async), later optional mediator library             |
| IRepository<T>    | Protocol + SQLAlchemy impl (when persistence introduced)               |
| DTO / ViewModel   | Pydantic models (DTO in application + response models in presentation) |
| IOptions<T>       | Pydantic BaseSettings                                                  |
| AutoMapper        | Explicit mapping functions or Pydantic model constructors              |
| FluentValidation  | Pydantic validators                                                    |
| Logging (ILogger) | Python `logging` + structured (JSON) fields                            |
| BackgroundService | FastAPI background tasks, Celery/RQ (future)                           |

React side:

- Use TypeScript interfaces instead of implicit any.
- Encapsulate server state with React Query (future) or simple fetch first.

---

## 7. AI / LLM Integration Guidelines

Current Phase: Placeholder → OpenAI (gpt-4o-mini) → Extended tooling.

Rules:

1. Provide an `AIProvider` interface (already present) with async methods: `explain(code)`, future: `generate_tests(code, language?)`, `refactor(code, goal?)`.
2. Avoid scattering prompt templates inline; centralize in `infrastructure/ai/prompts/`.
3. Use deterministic-ish parameters for explanation (e.g., temperature 0.2–0.4) unless creativity desired.
4. Provide structured outputs: backend returns JSON with explicit metadata fields (e.g., `explanation`, `line_count`, `char_count`, `provider`, `placeholder`).
5. When adding test generation/refactor:
   - Add new command & handler.
   - Extend dispatcher.
   - Update shared schema generation script for TS.
6. MCP (later): Provide tool schema definitions in a shared subdirectory (`/shared/schemas/tool_schemas.json` or under backend + codegen). Copilot should not create full MCP server prematurely.

---

## 8. Prompt Design (For Future AIProvider Enhancements)

- Keep prompts modular: `system`, `task`, `style`, `format`.
- Use explicit JSON schema shaping when asking for structured results to reduce parsing errors.
- Provide examples (few-shot) only if value > token cost.
- Maintain versioned prompt fragments; increment a `PROMPT_VERSION` constant on breaking changes.

---

## 9. Coding Standards

Backend (Python):

- PEP 8; line length <= 100.
- Type hints mandatory (mypy strict mode).
- Ruff for lint + (optionally) formatting.
- Public functions & classes: Google-style docstrings reflecting purpose and side effects.
- Avoid giant functions (>40 lines unless justified).
- Do not perform network I/O in constructors.

Frontend (React/TS):

- Strict TS config (no implicit any).
- Presentational vs container separation (where complexity warrants).
- Use functional components & hooks.
- Derive state; avoid duplicative local state.
- Provide explicit return types for public functions.
- Keep components focused (<250 lines).
- Prefer composition over adding props complexity; extract hooks for data logic (`useExplainCode` etc.).

---

## 10. Error Handling

Backend:

- Define custom exception hierarchy when domain/application errors emerge (e.g., `DomainError`, `ValidationError`, `AIProviderError`, `InfrastructureError`).
- Add FastAPI exception handlers mapping to clean JSON with `type`, `message`, optional `details`.
- Never leak raw stack traces to client in production.

Frontend:

- Graceful fallback UI states: loading, empty, error.
- Consider Error Boundary for future complex hierarchies.
- Provide user-friendly messages; log technical details to console only.

---

## 11. Testing Strategy

Backend:

- Unit tests per handler (mock AIProvider).
- Integration tests hitting API routes with `httpx.AsyncClient`.
- Golden tests (later) for LLM responses with semantic assertions (e.g., key sections present) rather than brittle exact string comparison.
- Use pytest fixtures to create `test_app` with dependency overrides.

Frontend:

- Soon: Add vitest + React Testing Library.
- Test critical flows: submitting explain request, handling errors.
- Snapshot only for stable presentational structures (avoid overuse).

CI (later):

- Lint, type check, test (fail fast).
- Possibly separate job matrix for backend/frontend.

---

## 12. Performance Guidelines

- Async endpoints; avoid blocking CPU-bound tasks inside event loop (defer to thread pool if needed).
- Batch model calls only when beneficial; maintain low latency.
- Cache invariant prompt fragments or compiled regex.
- Keep response payloads minimal.

---

## 13. Security & Privacy

- Never commit real API keys; enforce `.env.example`.
- Rate limit (future) to protect from accidental high-volume calls.
- Validate input size (max code length) to avoid runaway token usage.
- Sanitize logs (no secrets; optionally redact code if privacy required).
- Add CORS restrictions via settings for deployed environments.

---

## 14. Logging & Observability

- Use structured logs: `{"ts": "...", "level": "INFO", "event": "ai_call", "model": "...", "duration_ms": ...}`.
- Add correlation IDs (header `X-Request-ID`) in middleware (future).
- Summarize token usage (when available) for cost tracking.

---

## 15. Git & Workflow

Branch Naming:

- `feature/<short-desc>`
- `fix/<short-desc>`
- `chore/<short-desc>`
- `docs/<short-desc>`

Commit Message Conventions (Conventional Commit style recommended):

- `feat(explain): add OpenAI provider`
- `refactor(application): extract dispatcher logic`

PR Checklist (Copilot to help generate if requested):

- [ ] Linked ADR (if architectural change)
- [ ] Tests added/updated
- [ ] Updated docs / README section if user-facing change
- [ ] No layer violations
- [ ] Lint & type checks pass locally

---

## 16. ADR Process

- Place new ADR in `docs/architecture/adr-YYYYMMDD-<topic>.md` or sequential numeric (`adr-0002-openai-provider.md`).
- Status: proposed → accepted → superseded.
- Keep decision statements concise; include alternatives & consequences.

Copilot: When generating new features that change architectural direction, propose an ADR stub.

---

## 17. Extensibility Roadmap (High-Level)

(Details in `project-scope.md`)

1. Explain (placeholder) → Real AI.
2. Add Generate Tests & Refactor commands.
3. Shared schema export & TS codegen.
4. Chat orchestrator + tool selection.
5. MCP integration (tool registry).
6. Persistence (PostgreSQL) + repositories.
7. Auth (JWT) & user sessions.
8. Cost & usage analytics.
9. Optional RAG/embedding support (explain file trees / repositories).

---

## 18. When NOT to Over-Engineer

Copilot must avoid:

- Adding a database before persistence requirements.
- Introducing a mediator library before multiple handlers create complexity.
- Implementing full repository pattern for in-memory or one-off operations.
- Generating excessive abstraction layers for one method classes.
- Premature microservices split.

---

## 19. Anti-Patterns to Avoid

- Massive God handlers mixing formatting + business concerns.
- Returning raw provider responses directly to the client.
- Hidden global state for configuration.
- Circular imports due to cross-layer coupling.
- Copy-pasted prompt fragments with slight shifts (centralize them).
- Embedding infrastructure logic (OpenAI SDK calls) inside domain or presentation layers.

---

## 20. Frontend Interaction Guidelines

- Provide an API service layer (`/src/services/api.ts`) abstracting fetch/axios calls.
- Use discriminated unions (later) for tool response types (`type ToolResponse = ExplainResponse | RefactorResponse | TestSuggestionsResponse`).
- When code generation grows: add code-splitting to keep bundle lean.

---

## 21. Code Generation (Later Phase)

- Pydantic models → JSON Schema → TS interfaces (script).
- Copilot must not hand-maintain TS types once codegen is enabled; instead, modify Python models and re-run script.

---

## 22. MCP & Tooling (Future Guidance)

- Define tool JSON schema (name, description, input schema, output schema).
- Provide an internal `ToolRegistry` service mapping intent to command dispatch.
- Eventually support chat classification → tool invocation -> streaming results (if needed).
- Avoid locking into a single vendor; AIProvider should be swappable.

---

## 23. Example Command Addition Workflow (Copilot Reference)

1. Add command dataclass: `GenerateTestsCommand(code: str, language: str | None)`.
2. Add result DTO: `TestSuggestionsResultDTO`.
3. Implement handler calling `AIProvider.generate_tests`.
4. Extend `AIProvider` interface & Fake implementation.
5. Register handler in dispatcher.
6. Create new router endpoint `/api/v1/tests` returning the DTO.
7. Update shared schema & regenerate TS.
8. Add unit tests & integration route test.
9. Document in `project-scope.md` status or create ADR if design shift.

---

## 24. Asking for Clarification

Copilot should ask before proceeding when:

- User requests persistence but no schema defined.
- Conflicting architecture instructions appear.
- Adding dependencies with overlapping purpose (e.g., both dependency-injector and a manual container).
- Unclear whether feature should be synchronous or background.

---

## 25. Glossary

- ADR: Architectural Decision Record.
- CQRS: Command Query Responsibility Segregation.
- DTO: Data Transfer Object.
- MCP: Model Context Protocol (tool selection/orchestration).
- Provider: Implementation of `AIProvider` interface.
- Vertical Slice: End-to-end narrow feature pipeline.

---

## 26. Quick Reference Checklist (Copilot Autocomplete Heuristics)

Before suggesting code:

- Is this the correct layer?
- Are imports respecting dependency direction?
- Are types and docstrings provided?
- Will tests be easy to add?
- Is this aligned with current phase (see project-scope)?
- Have I avoided premature optimization?

---

## 27. Sample Minimal Handler Pattern (Canonical)

```python
@dataclass(frozen=True)
class SomeCommand:
    value: str

class SomeResultDTO(BaseModel):
    processed: str

class SomeHandler:
    def __init__(self, dependency: SomePort) -> None:
        self._dependency = dependency

    async def handle(self, command: SomeCommand) -> SomeResultDTO:
        raw = await self._dependency.process(command.value)
        return SomeResultDTO(processed=raw.upper())
```

---

## 28. Updating These Instructions

Any substantial update → new ADR referencing the change.  
Keep this file cohesive; prune obsolete instructions.

---

## 29. Summary for Copilot

When generating or modifying code:

1. Choose the correct layer and respect boundaries.
2. Encapsulate LLM interactions behind `AIProvider`.
3. Add or update commands & handlers for new use cases (CQRS style).
4. Maintain strict typing & docstrings.
5. Provide tests unless explicitly deferred.
6. Reference `docs/project-scope.md` for phase alignment.
7. Avoid over-engineering; escalate with a clarifying question if direction uncertain.

End of copilot-instructions.
