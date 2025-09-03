# AI Code Assistant

An incremental, Clean Architecture–driven AI development tool that:

- Explains arbitrary code snippets in plain English
- Suggests refactors for clarity / maintainability
- Generates unit test scaffolds
- Evolves into a chat + tool (MCP-style) orchestrated assistant
- Later adds persistence (history), authentication, cost tracking, and optional advanced features (RAG, diff-based refactors)

> This repository is intentionally built **vertically slice by slice**. Early commits stay lean; complexity (DB, auth, MCP protocol wiring) is introduced only when its phase arrives.

---

## Table of Contents

1. Vision & Value
2. Feature Roadmap (Phases)
3. Architecture Overview
4. High-Level Flow (Explain Slice)
5. Directory Structure
6. Technology Choices
7. Getting Started
8. Environment Variables
9. Development Scripts & Tooling
10. Quality Standards (Lint, Types, Tests)
11. Adding a New Use Case (Command Pattern Walkthrough)
12. AI Provider Abstraction
13. Future: Schema Code Generation (TS from Pydantic)
14. MCP / Tool Orchestration (Planned)
15. ADR Process
16. Contributing Workflow
17. Security & Privacy
18. Performance & Observability Plan
19. FAQ
20. Roadmap Status
21. License
22. Acknowledgements

---

## 1. Vision & Value

Developers often need rapid insight into unfamiliar code: what it does, how to improve it, and how to test it. This project offers a single UI + API that grows from basic explanations into a robust “LLM tool conductor,” emphasizing maintainable architecture and clear extensibility—ideal for demonstrating transition from a .NET / Clean Architecture background into Python + React + AI orchestration.

---

## 2. Feature Roadmap (Phases)

| Phase | Focus                       | Summary                                                   |
| ----- | --------------------------- | --------------------------------------------------------- |
| 1     | Foundations                 | Backend + frontend skeleton, placeholder explain endpoint |
| 2     | Real AI                     | OpenAI-powered explanation, provider abstraction          |
| 3     | Multi-Tool                  | Refactor + Test Generation commands/endpoints             |
| 4     | Shared Schemas & Chat       | Pydantic → TS codegen; natural language routing (basic)   |
| 5     | MCP Integration             | Tool registry + LLM tool/function calling orchestration   |
| 6     | Persistence & Observability | PostgreSQL history, logging, correlation IDs              |
| 7     | Auth & Cost Tracking        | JWT auth, token/cost metrics                              |
| 8+    | Advanced                    | Streaming, RAG, diff refactors, multi-file context        |

See: `docs/project-scope.md` for deeper detail.

---

## 3. Architecture Overview

Layered Clean Architecture:

```
(frontend) -> HTTP JSON -> Presentation (FastAPI routers)
  -> Application (Commands / Handlers / DTOs / Dispatcher)
    -> Domain (Value Objects, Entities, Domain Services)
    -> Infrastructure (AI Provider, later Persistence, External APIs)
```

Principles:

- Dependency direction: outer → inner only
- Domain pure (no FastAPI / OpenAI imports)
- Application orchestrates; no framework leakage upward
- Infrastructure implements interfaces defined in Application
- Presentation handles HTTP mapping only

---

## 4. High-Level Flow (Explain Slice)

```
POST /api/v1/explain
  -> Presentation builds ExplainCodeCommand
  -> Dispatcher finds ExplainCodeHandler
  -> Handler creates CodeSnippet (domain)
  -> Calls AIProvider.explain_code(snippet)
  -> Returns ExplanationResultDTO
  -> Response serialized to client
  -> Frontend renders explanation metadata
```

---

## 5. Directory Structure (Initial)

```
backend/
  app/
    domain/
      code_snippet.py
    application/
      commands/
      handlers/
      dto/
      interfaces/
      dispatch.py
    infrastructure/
      ai/
        fake_provider.py
        (openai_provider.py – Phase 2)
    presentation/
      api/v1/
        explain_router.py
      dependencies.py
      startup.py
    main.py
  tests/
frontend/
  src/
    components/
    pages/
    hooks/
    services/
      api.ts
    types/
    utils/
docs/
  project-scope.md
  architecture/
    overview.md
    adr-0001-monorepo.md
.github/
  copilot-instructions.md
```

Future additions:

- `shared/` for tool schemas & generated types
- `migrations/` (after persistence)
- `infra/` (Docker, CI/CD, deployment manifests)

---

## 6. Technology Choices

| Concern            | Choice                                 | Rationale                                        |
| ------------------ | -------------------------------------- | ------------------------------------------------ |
| Backend Framework  | FastAPI                                | Async-first, type-friendly                       |
| Python Version     | 3.12                                   | Performance, typing improvements                 |
| AI Model (initial) | OpenAI gpt-4o-mini                     | Balance speed/cost                               |
| Package Mgmt       | Poetry (or uv)                         | Reproducible, pyproject-based                    |
| Lint / Format      | Ruff (+ mpy)                           | Unified lint/format, speed                       |
| Types              | mypy strict                            | Reliability, translation from .NET strong typing |
| Frontend           | React + Vite + TS                      | Fast dev, strict types                           |
| Editor             | Monaco                                 | Rich language support                            |
| Tests              | pytest / React Testing Library (later) | Standard ecosystems                              |

---

## 7. Getting Started

Prerequisites:

- Python 3.12
- Node 18+
- (Optional Phase 2+) OpenAI API key

Clone & bootstrap:

```bash
git clone <repo-url>
cd <repo-root>

# Backend
cd backend
poetry install
poetry run uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

---

## 8. Environment Variables

`backend/.env.example` (copy to `.env`):

| Variable        | Purpose                          | Phase |
| --------------- | -------------------------------- | ----- |
| OPENAI_API_KEY  | Unlock real AI provider          | 2     |
| OPENAI_MODEL    | Model name (default gpt-4o-mini) | 2     |
| LOG_LEVEL       | Logging verbosity                | 2+    |
| ALLOWED_ORIGINS | CORS config                      | 1     |

---

## 9. Development Scripts & Tooling

Backend (Poetry examples):

```
poetry run uvicorn app.main:app --reload
poetry run ruff check .
poetry run ruff format .
poetry run mypy .
poetry run pytest -q
```

Frontend:

```
npm run dev
npm run build
npm run lint
```

Planned:

- GitHub Actions: lint/type/test matrix (added after Phase 2 or 3)
- Docker Compose: backend + frontend + db (Phase 6)

---

## 10. Quality Standards

Backend:

- Strict typing, no implicit `Any`
- Docstrings (Google style) on public handlers & interfaces
- Functions < ~40 lines preferred
- Domain free of IO / frameworks

Frontend:

- TS strict mode
- Avoid duplicating server state; centralize API calls in `services`
- Presentational vs data hooks separation

Testing Progression:

- Phase 1–2: Unit tests for handlers + basic route integration
- Phase 3: Add tests for each new command
- Phase 4+: Add schema/codegen drift tests
- Phase 6+: Database integration tests (transaction rollbacks)

---

## 11. Adding a New Use Case (Command Pattern Walkthrough)

Example: Add “Generate Tests”

1. Domain: (Often none needed initially beyond raw code snippet)
2. Application:
   - Create `GenerateTestsCommand(code: str, language: str|None)`
   - Create `TestSuggestionsResultDTO`
   - Extend `AIProvider` with `generate_tests()`
   - Implement `GenerateTestsHandler`
   - Register handler in `build_dispatcher`
3. Infrastructure:
   - Implement method in Fake + OpenAI provider
   - Add prompt fragment
4. Presentation:
   - Add router `/api/v1/tests`
   - Add request/response models (reuse DTO or adaptor)
5. Frontend:
   - Add API function + UI button
6. Tests:
   - Handler unit test (AIProvider mocked)
   - Route integration test
7. Docs:
   - Update `project-scope.md` Phase 3 progress
   - (If architectural shift) new ADR

---

## 12. AI Provider Abstraction

Interface (simplified):

```python
class AIProvider(ABC):
    async def explain_code(self, code: str) -> str: ...
    async def generate_tests(self, code: str, language: str | None = None) -> str: ...
    async def refactor(self, code: str, goal: str | None = None) -> str: ...
```

Providers:

- `FakeAIProvider` (deterministic placeholder)
- `OpenAIProvider` (Phase 2)
- Future: Additional vendors or local model

---

## 13. Future: Schema Code Generation

Goal: Avoid manually syncing DTO definitions between backend & frontend.

Workflow (Phase 4):

1. Export Pydantic models to JSON Schema.
2. Run codegen script to produce `frontend/src/types/generated.ts`.
3. Import generated types in API layer.
4. CI check ensures regenerated output matches committed file (drift detection).

---

## 14. MCP / Tool Orchestration (Planned)

- Define internal `ToolDescriptor` objects referencing command input/output.
- Provide JSON schema for each tool to LLM function-calling interface.
- Chat endpoint decides tool invocation either:
  - Lightweight classifier (keywords)
  - LLM tool selection function-calling (structured)
- Source of truth: Python DTOs → schema export → used by chat orchestrator.

---

## 15. ADR Process

1. Create new file: `docs/architecture/adr-YYYYMMDD-topic.md`
2. Include: Status, Context, Decision, Consequences, Alternatives
3. Reference ADR in PR description
4. Supersede by linking forward/backward

Existing:

- ADR-0001: Monorepo decision

---

## 16. Contributing Workflow

1. Create branch: `feature/<short-desc>`
2. Make changes + add/update tests
3. Run quality checks locally
4. Open PR: include rationale, link ADR if architectural change
5. Ensure CI passes before review
6. Squash merge (keep linear history)

Commit Message Style (Conventional):

```
feat(explain): integrate OpenAI provider
refactor(application): extract base handler
test(presentation): add integration tests for /tests endpoint
```

---

## 17. Security & Privacy

- Never commit secrets; always `.env` + secret manager in deployment.
- Input size guard (future) to prevent excessive token spend.
- Log redaction for secrets.
- CORS restricted via settings for non-local environments.
- Rate limiting (future) before public exposure.

---

## 18. Performance & Observability Plan

Later middleware:

- Request timing
- Correlation ID (`X-Request-ID`)
- Structured logs: `{event, command, duration_ms, model, success}`
  Add metrics endpoint (optional) using Prometheus client when complexity increases.

---

## 19. FAQ

Q: Why not start with a DB?
A: Reduces early complexity; persistence only when history feature arrives (Phase 6).

Q: Why custom dispatcher vs external mediator?
A: Keeps dependencies lean until multiple handlers & cross-cutting behaviors justify adoption.

Q: Can we add streaming now?
A: Deferred; first stabilize synchronous flows & structured outputs.

Q: Why OpenAI vs local model?
A: Fast path to feature completeness; pluggable provider supports future swap.

---

## 20. Roadmap Status

(Keep updated manually or generate from script later.)

| Phase | Status                        | Notes                    |
| ----- | ----------------------------- | ------------------------ |
| 1     | In Progress / Done (scaffold) | Placeholder explain live |
| 2     | Pending                       | OpenAI provider next     |
| 3     | Pending                       | Multi-tool endpoints     |
| 4     | Pending                       | Chat + schema codegen    |
| 5     | Pending                       | MCP integration          |
| 6     | Pending                       | Persistence & logs       |
| 7     | Pending                       | Auth + cost              |
| 8+    | Backlog                       | Advanced features        |

---

## 21. License

TBD (Recommend: MIT for openness & portfolio use).

---

## 22. Acknowledgements

- Clean Architecture & DDD inspiration from classic literature & community patterns.
- OpenAI models for initial LLM functionality.
- Monaco Editor for in-browser code editing.

---

## Quick Reference Cheat Sheet

| Action            | Command                                               |
| ----------------- | ----------------------------------------------------- |
| Run backend       | `poetry run uvicorn app.main:app --reload`            |
| Run backend tests | `poetry run pytest -q`                                |
| Lint + format     | `poetry run ruff check . && poetry run ruff format .` |
| Type check        | `poetry run mypy .`                                   |
| Run frontend      | `npm run dev`                                         |
| Build frontend    | `npm run build`                                       |

---

For architectural guidance & coding conventions see:

- `.github/copilot-instructions.md`
- `docs/project-scope.md`
- `docs/architecture/overview.md`
