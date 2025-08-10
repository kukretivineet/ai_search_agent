# Copilot Instructions (Repository-wide)

This repository uses Python 3.11+, FastAPI, Pydantic v2, Uvicorn, and MongoDB (Atlas) via Motor. The architecture follows Clean Code and Domain-Driven Design (DDD). Use these rules when generating or editing code.

## Goals

- Clean, typed, async-first APIs.
- Clear separation of concerns with DDD modules and layers.
- Strong lint/type/security checks.
- High performance semantic search system per PLANE.TXT.

## Project Architecture

Follow DDD-inspired structure for new features and services:

- app/
  - main.py (FastAPI app factory + routers registration)
  - core/
    - config.py (pydantic-settings; env-based configuration)
    - logging.py (structured logging via structlog)
  - db/
    - mongo.py (Motor client factory + lifecycle hooks)
  - api/
    - v1/
      - routes/ (APIRouter per domain)
      - schemas/ (Pydantic models for requests/responses)
      - deps.py (Depends utilities: settings, db, auth)
      - services/ (Application services; orchestrate repositories)
      - repositories/ (DB access helpers; Motor queries)
  - domain/
    - <bounded_context>/
      - models.py (Entity/ValueObject Pydantic models)
      - services.py (Domain services, pure business logic)
      - events.py (Domain events if any)
  - tests/
    - unit/ (pure functions/domain/services)
    - api/ (pytest + httpx.AsyncClient)
    - integration/ (Motor test db / mongomock_motor)

## Coding Standards

- Use async FastAPI endpoints and Motor (async) for MongoDB.
- Pydantic v2 models for request/response validation. Include types, examples, and field descriptions.
- Type hints everywhere. Docstrings in Google style.
- Logging: structlog preferred; avoid logging secrets.
- Do not construct Mongo queries via string concatenation.
- Convert MongoDB ObjectId to str in responses.
- Pagination: cursor/offset with max limits; validate inputs.
- Feature flags via settings when appropriate.

## Linting/Formatting/Typing

- Formatting: black (line length 100), isort (profile=black).
- Linting: ruff (enable flake8, pyflakes, pycodestyle, bugbear; treat warnings as errors).
- Typing: mypy (strict-ish; disallow-any-generics=true, allow-redefinition=false).

## FastAPI Patterns

- App factory pattern that injects settings and dependencies.
- APIRouter per domain, mounted under /api/v1.
- Use Depends for settings, db clients, and auth.
- Return explicit ResponseModel objects, not raw DB docs.
- Add error handlers for HTTPException and pydantic.ValidationError.

## MongoDB (Motor) Patterns

- Single global Motor client created at startup; close on shutdown.
- Create compound indexes where needed; emit create_index calls.
- Always pass session for multi-write operations if transactions are used.
- Store vectors and metadata fields explicitly; keep embeddings in arrays of float.

## Testing

- pytest + httpx.AsyncClient for endpoint tests (async).
- Use a test database (or mongomock_motor) and fixture isolation.
- Cover happy paths and validation errors.
- Add minimal seed data builders/factories for domain objects.

## Semantic Search Guidance (from PLANE.TXT)

- Implement intent parsing that extracts facets (color, price range, recipient, occasion, eco flags, refurbished, size, brand, delivery constraints) into a validated Pydantic object with a confidence score. If confidence < 0.8, fallback to regex/keyword-only filters.
- Hybrid retrieval: run vector (Atlas $vectorSearch) and BM25 text search in parallel, normalize scores, and blend with initial weights 0.6/0.4. Make weights configurable.
- Reranking: optional Cohere/OpenAI/Local MiniLM reranker on top-K; use MMR to diversify.
- Caching: cache per query hash with TTL; skip rerank when cosine > 0.92.
- Evaluation: keep IR metrics (NDCG, Recall) and latency; fail CI if drops exceed thresholds.
- Synonyms: maintain Atlas Search synonyms for cross-category terms; load from JSON.
- Schema: support universal attributes and dynamic per-category facets.

## Commit Messages & PRs

- Conventional Commits (feat:, fix:, docs:, refactor:, test:, chore:).
- Each PR must include:
  - Description of changes and rationale.
  - Screenshots/metrics for performance-affecting changes.
  - Checkboxes indicating tests added/updated and docs updated.

## Example Snippets

- Use APIRouter, async dependencies, Motor collection access via repository layer.
- Unit tests should use pytest-asyncio and httpx.AsyncClient.

Adhere strictly to these rules when proposing code or scaffolding files for this repository.
