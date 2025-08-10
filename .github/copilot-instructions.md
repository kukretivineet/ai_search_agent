# Copilot Instructions (Repository-wide)

## Project context

- Stack: Python 3.11+, FastAPI, Pydantic v2, Uvicorn, MongoDB (Atlas) via Motor (async).
- Goals: Clean, typed, async-first APIs with clear separation of concerns and strong lint/type checks.
- Architecture: Clean Code + Domain-Driven Design (DDD) with clear layers and bounded contexts.

## How to generate code in this repo

1. Always use async FastAPI endpoints and Motor for MongoDB (no sync PyMongo in APIs).
2. Use Pydantic v2 models for request/response validation. Include field types, descriptions, and examples.
3. Add Google-style docstrings and type hints everywhere.
4. Log with structlog or logging (structured where possible). Never log secrets or raw tokens.
5. Provide unit tests (pytest) when creating or changing modules; cover happy paths and validation errors.
6. Respect the project layout below and DDD boundaries (routes -> services -> repositories).
7. Convert MongoDB ObjectId to str in all API responses; never return raw DB docs.
8. Create compound indexes where needed; emit create_index calls.
9. Avoid string-built queries. Build typed filter dicts. Validate all inputs with Pydantic.
10. Enforce formatting (black, isort), linting (ruff), and typing (mypy). Max line length 100.

## Project layout (follow when scaffolding)

app/
main.py # FastAPI app factory + routers registration
core/
config.py # Settings via pydantic-settings
logging.py # Logging configuration (structlog)
db/
mongo.py # Motor client + lifecycle (startup/shutdown)
api/
v1/
routes/ # APIRouters per domain
schemas/ # Pydantic models (request/response)
deps.py # Depends(...) utilities (settings, db, auth)
services/ # Application services (use-case orchestration)
repositories/ # DB access helpers (Motor queries)
domain/
<bounded_context>/
models.py # Entities/ValueObjects (Pydantic where helpful)
services.py # Domain services (pure business logic)
events.py # Domain events (optional)
tests/
unit/ # Pure/domain/service tests
api/ # FastAPI endpoint tests (httpx.AsyncClient)
integration/ # Motor test DB / mongomock_motor fixtures

## Coding standards

- Formatting: black (line length 100), isort (profile=black).
- Linting: ruff (enable flake8, pyflakes, pycodestyle, bugbear; treat warnings as errors).
- Typing: mypy (strict-ish; allow-redefinition = false, disallow-any-generics = true).
- Security: Do not log PII/secrets; validate and bound all inputs; sanitize outbound errors.

## FastAPI patterns

- Create an app = FastAPI() via an app factory that injects settings.
- Use APIRouter per domain; mount under /api/v1.
- Use Depends for settings, db clients, and auth.
- Return ResponseModel with explicit fields (no raw DB documents).
- Add error handlers for HTTPException, pydantic.ValidationError.

## MongoDB patterns (Motor)

- Use a single global Motor client created at startup; close on shutdown.
- Create compound indexes where needed; ask Copilot to emit create_index calls.
- Always pass session for multi-write operations if transactions are used.
- Convert \_id (ObjectId) to string in responses.
- Store vector embeddings as arrays of float.

## Testing

- Use pytest + httpx.AsyncClient for endpoint tests (async).
- Use a test database (or mongomock_motor if suitable) and fixture isolation.
- Cover happy path + validation errors. Include minimal seed/builders.

## Semantic Search Guidance (from PLANE.TXT)

- Intent Parsing
  - Few-shot GPT-4o-mini (or configured LLM) JSON extractor + Pydantic validation.
  - Extract facets: color, size, material, brand, price ranges, recipient, occasion, eco/refurbished flags, delivery/budget, warranty, bundles.
  - Provide confidence score; if < 0.8 → fallback to regex/keyword-only filters.
- Retrieval
  - Run vector search (Atlas $vectorSearch) and BM25 text search in parallel.
  - Build structured filter query from parsed facets (price, in_stock, eco_cert, brand...).
- Score Fusion + Boost
  - Normalize scores and blend (default weights: vector 0.6, bm25 0.4). Make configurable.
  - Optional boosts: popularity, freshness.
- Reranking & Diversity
  - Rerank top-K via Cohere/OpenAI/Local MiniLM; apply MMR for diversity.
  - Skip rerank when cosine similarity > 0.92 to save cost/latency.
- Gift/Bundles
  - If query implies recipient/occasion or bundles, trigger secondary agent to compose complementary SKUs; return grouped results.
- Synonyms & Ontology
  - Maintain Atlas Search synonyms for cross-category terms (e.g., cell ↔ mobile, hoodie ↔ sweatshirt).
  - Support universal attributes and dynamic per-category facets.
- Caching & Latency
  - Cache by SHA256(query + locale) with TTL 24h, LRU eviction.
  - Async/parallelize using asyncio + Motor; target sub-400 ms p95.
- Evaluation & CI Gates
  - Track NDCG, Recall, latency; fail CI if NDCG@10 drops > 5% or latency rises > 20%.
  - Keep a gold set across categories and nightly replay of top queries.
- Governance
  - Alert/fallback when parser confidence is low; ensure GDPR-compliant logs.

## Commit messages & PRs

- Conventional Commits: feat:, fix:, docs:, refactor:, test:, chore:.
- Each PR must include:
  - Description and rationale.
  - Tests updated/added; docs updated where needed.
  - Index changes/migrations noted.
  - Performance metrics if retrieval/rerank logic changed.

## Docstrings & comments

- Use Google-style docstrings:
  Args:
  Returns:
  Raises:
