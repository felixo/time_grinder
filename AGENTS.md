# AGENTS.md

## Purpose

This file defines how coding agents should work inside the Time Grinder repository.

Before making changes, read:

- `docs/product.md`
- `docs/architecture.md`
- `docs/ux/main-screen.md`

These documents are the current source of truth for product and architecture decisions.

Do not silently override them.

## Project stack

Frontend:
- React
- TypeScript
- Vite

Backend:
- Python
- Django
- Django Ninja
- Django ORM
- PostgreSQL

Tooling:
- `uv` for Python dependency management
- `npm` for frontend dependency management
- Django migrations for database schema changes
- `pytest` + `pytest-django` for backend tests
- Vitest + React Testing Library for frontend tests
- Docker Compose for local PostgreSQL

Future platform targets:
- Web
- Telegram Mini App
- Capacitor / iOS

## General working rules

Before implementing a task:

1. Read the relevant documentation.
2. Inspect existing code and patterns.
3. Prefer the simplest implementation consistent with the architecture.
4. Avoid introducing new abstractions without a concrete need.
5. Keep changes focused on the requested task.

Do not redesign the architecture unless explicitly asked to do so.

## Scope discipline

Do not:
- refactor unrelated code;
- introduce new frameworks without explicit approval;
- introduce new dependencies unless necessary;
- add speculative infrastructure;
- add Redis, queues, WebSockets, GraphQL, microservices or similar systems unless explicitly requested;
- create separate frontend implementations for Web, Telegram and iOS;
- introduce SQLAlchemy or Alembic;
- replace Django ORM or Django migrations;
- add state-management libraries unless existing React state is clearly insufficient.

## Project commands

Before backend commands, load the root `.env` into the shell and select the
dedicated environment (run from the repository root):

```bash
set -a
source .env
set +a
export UV_PROJECT_ENVIRONMENT="$(pyenv prefix)"
```

Before frontend commands, select the pinned Node version:

```bash
eval "$(fnm env --shell bash)"
fnm use
```

See README.md for one-time runtime and environment setup.

### Database

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Check PostgreSQL:

```bash
docker compose ps
```

Stop local services:

```bash
docker compose down
```

Reset local PostgreSQL data only when explicitly requested:

```bash
docker compose down -v
```

Do not destroy local database volumes as part of normal task completion.

### Backend setup

```bash
cd backend
export UV_PROJECT_ENVIRONMENT="$(pyenv prefix)"
uv sync
```

Apply migrations:

```bash
cd backend
uv run python manage.py migrate
```

Create migrations after model changes:

```bash
cd backend
uv run python manage.py makemigrations
```

Run the backend development server:

```bash
cd backend
uv run python manage.py runserver
```

Run backend tests:

```bash
cd backend
uv run pytest
```

### Frontend setup

Install dependencies:

```bash
cd frontend
npm install
```

Run the frontend development server:

```bash
cd frontend
npm run dev
```

Run frontend tests:

```bash
cd frontend
npm test
```

If the actual generated `package.json` uses a different test command, update both this file and `README.md` to match the real project.

Additional scaffold checks:

```bash
cd backend
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py migrate --check
```

From `frontend/`, run `npm run build` to check TypeScript and build production assets.
No separate linter or formatter is currently configured.

## Local development expectations

Local development should use:

- PostgreSQL via Docker Compose;
- Django locally through `uv`;
- React/Vite locally through `npm`.

Backend and frontend do not need to run inside Docker during normal development.

The expected startup sequence is:

1. start PostgreSQL;
2. apply Django migrations;
3. start Django;
4. start Vite.

The root `README.md` should contain complete human-facing setup instructions.

This file should contain the exact commands coding agents are expected to use.

## Environment configuration

Local configuration should be provided through environment variables.

The repository should contain a safe `.env.example`.

Do not commit real credentials, API keys, passwords or production secrets.

The local PostgreSQL configuration should be documented in `.env.example` and `README.md`.

When adding a new required environment variable:

1. add it to `.env.example`;
2. document its purpose;
3. update local setup instructions if necessary.

## Backend rules

The backend uses Django + Django Ninja.

Use Django ORM for persistence.
Use Django migrations for schema changes.

The backend is the source of truth for:
- persisted data;
- timer state;
- business rules;
- reports;
- user data isolation;
- domain invariants.

Keep PostgreSQL access behind the Django backend.

Do not expose database implementation details directly through the API.

## Django structure

Prefer a pragmatic Django structure.

The MVP should begin with the primary `grinder` Django app.

Do not split the project into many Django apps without a clear reason.

Business logic that does not belong directly in API handlers should live in service/domain code.

Keep API handlers thin where practical.

## User model

Use a custom Django User model from the beginning.

The application must support multiple users in the data model even though the MVP may use a predefined/default user.

User-facing time calculations must respect the user's configured timezone.

## Timer rules

A running timer is represented as an unfinished Action.

```text
started_at != NULL
ended_at = NULL
duration_seconds = NULL
```

A user may have at most one running Action.

This invariant should be enforced in backend logic and, where practical, by the database.

The frontend timer display is calculated locally from `started_at`.

Do not send API requests every second to update the timer.

## Manual Action rules

Manual time entry stores a duration without inventing a precise historical start/end time.

```text
started_at = NULL
ended_at = NULL
duration_seconds = 1800
```

Do not fabricate timestamps for manually entered duration.

## Undo rules

Undo is a product operation.

Frontend code should call the backend Undo API rather than reconstructing Undo logic locally.

For the MVP, Undo may delete the most recent eligible Action.

## API rules

Use REST over HTTPS/JSON.

Prefer product-oriented endpoints such as:

```text
POST /api/timer/start
POST /api/timer/stop
POST /api/undo
GET  /api/reports/today
```

Do not make the frontend responsible for backend domain behavior.

Do not introduce GraphQL or WebSockets unless explicitly requested.

## Frontend rules

The frontend is mobile-first.

Most frontend code should be platform-agnostic.

Platform-specific behavior belongs behind the `platform` abstraction.

Initial structure:

```text
frontend/src/
├── pages/
├── components/
├── api/
├── domain/
└── platform/
```

Do not create a global `store` directory or introduce Redux/Zustand/etc. unless there is a concrete need.

Prefer local React state and small focused abstractions initially.

## Platform rules

Web is the first implementation target.

Telegram and Capacitor/iOS are future targets.

Do not implement Telegram or Capacitor integration unless explicitly requested.

Do not let future platform support complicate the MVP unnecessarily.

When platform-specific behavior is required, isolate it behind the platform layer.

## UX rules

The main product interaction should remain:
- fast;
- mobile-first;
- usable with one hand;
- low-friction;
- easy to undo.

Prefer direct actions and Undo over confirmation dialogs.

Do not introduce multi-step forms for simple time tracking unless explicitly required.

Refer to `docs/ux/main-screen.md`.

## Database rules

PostgreSQL is the primary database.

Use Django ORM only.

Use Django migrations only.

Do not introduce SQLAlchemy or Alembic.

When changing models:

1. create Django migrations;
2. inspect the generated migration;
3. run migrations locally;
4. update tests if domain behavior changed.

Do not edit old migrations unless explicitly requested.

Database-level constraints should be used for important invariants where practical.

In particular, the one-running-timer-per-user rule should be protected by the database where possible.

## Django Admin

Django Admin is an internal development and operational tool.

It is not part of the end-user product UI.

It may be used to:
- inspect Users;
- inspect Actions;
- manage predefined Areas;
- manage predefined Projects;
- diagnose persisted data.

Do not build a custom end-user Area/Project editor for the MVP unless explicitly requested.

## Django Migrations
Never generate django migrations, alwas use: python manage.py makemigrations

## PostgreSQL runtime:
- use docker compose

## Backend runtime:
- use pyenv-managed Python
- use the dedicated pyenv virtualenv `3.12.8_time_grinder`
- create it with `pyenv virtualenv 3.12.8 3.12.8_time_grinder`
- set `export UV_PROJECT_ENVIRONMENT="$(pyenv prefix)"` before all uv commands
- use uv

## Frontend runtime:
- use fnm-managed Node
- use project-local node_modules
- use npm

Do not rely on globally installed Python or Node packages.

## Testing rules

For meaningful backend changes:
- add or update tests;
- run relevant `pytest` tests.

Important backend behavior includes:
- only one running timer per user;
- timer start/stop;
- manual Action creation;
- Undo;
- Today aggregation;
- user data isolation.

For meaningful frontend logic:
- add or update Vitest / React Testing Library tests where appropriate.

Do not add tests that only assert implementation details.

If a command cannot be run, clearly state why.

## Dependency changes

Before adding a dependency:

1. explain why it is needed;
2. prefer standard framework functionality where reasonable;
3. avoid adding libraries for trivial problems.

Do not add dependencies solely because they are popular or convenient.

## Documentation rules

Keep documentation synchronized with the real project.

When changing:
- setup steps;
- test commands;
- environment variables;
- project structure;
- architectural decisions;

update the relevant documentation.

Use:
- `README.md` for human-facing setup and local development instructions;
- `AGENTS.md` for agent-specific rules and exact task commands;
- `docs/architecture.md` for architectural decisions;
- `docs/product.md` for product requirements;
- `docs/ux/` for UX behavior.

## Completion checklist

Before finishing a task:

1. review the full diff;
2. remove unrelated changes;
3. run relevant tests;
4. run linters/formatters if configured;
5. verify migrations if models changed;
6. verify documented commands still match the project;
7. summarize what changed;
8. mention any tests or checks that could not be run;
9. call out any architectural decision that deserves explicit review.

## Git discipline

Keep changes small and task-focused.

Do not commit secrets.

Do not modify `.env` files containing real credentials.

Do not rewrite Git history unless explicitly requested.

Do not commit generated or local development artifacts unless the repository explicitly tracks them.
