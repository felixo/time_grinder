# Time Grinder

Mobile-first personal time tracking. The initial scaffold contains Django / Django
Ninja, PostgreSQL, and React / TypeScript / Vite. Time-tracking features are deferred.

## Prerequisites

Install `pyenv` with `pyenv-virtualenv`, `uv`, `fnm`, and Docker with Compose.
Start Docker Desktop on macOS. Application packages live only in the dedicated
Python environment and `frontend/node_modules`; no global packages are needed.

Commands assume Bash or Zsh and start from the repository root unless stated.
No global Python/Node version or shell profile changes are needed.

## Environment

On first setup, copy the example (do not overwrite an existing `.env`):

```bash
cp .env.example .env
```

Load it in each terminal running Django, migrations or backend tests:

```bash
set -a
source .env
set +a
```

Compose reads `.env` automatically. Django reads exported environment variables;
it does not load `.env` itself. Keep `.env` private and untracked.

| Variable | Purpose / local example |
| --- | --- |
| `DJANGO_SECRET_KEY` | Required signing key; example is for local development only |
| `DJANGO_DEBUG` | `true` for debugging; defaults to `false` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts, `localhost,127.0.0.1` |
| `POSTGRES_DB` | Required database name, `time_grinder` |
| `POSTGRES_USER` | Required database role, `time_grinder` |
| `POSTGRES_PASSWORD` | Required local database password |
| `POSTGRES_HOST` | Django database host, `127.0.0.1` |
| `POSTGRES_PORT` | Host database port, `55432`, also used by Compose |

PostgreSQL binds only to loopback on a dedicated port. The Compose project is
`time-grinder` with its own persistent volume. Choose another free port if needed.
Initialization variables apply only when the volume is first created; changing
`.env` does not change an existing database's credentials.

## Python and backend dependencies

Use Python 3.12.8 with the dedicated named virtualenv selected by `.python-version`:

```bash
pyenv install -s 3.12.8
pyenv virtualenv 3.12.8 3.12.8_time_grinder
pyenv local 3.12.8_time_grinder
export UV_PROJECT_ENVIRONMENT="$(pyenv prefix)"
cd backend
uv sync
```

Create the virtualenv only once; skip `pyenv virtualenv` if it already exists.
In each backend terminal, export `UV_PROJECT_ENVIRONMENT` from inside this repository
before using uv. This uses the named environment instead of `backend/.venv`.
No activation is needed for `uv run`. Dependencies are locked in `uv.lock`.

## Start local development

First, start PostgreSQL from the repository root:

```bash
docker compose up -d postgres
docker compose ps
```

Wait for healthy status. PostgreSQL is the only Dockerized service.

In a backend terminal, from the root:

```bash
set -a
source .env
set +a
export UV_PROJECT_ENVIRONMENT="$(pyenv prefix)"
cd backend
uv run python manage.py migrate
uv run python manage.py runserver
```

Health: <http://127.0.0.1:8000/api/health> returns `{"status":"ok"}`.
API docs: <http://127.0.0.1:8000/api/docs>.
Admin: <http://127.0.0.1:8000/admin/>. Optionally create an admin account using
`uv run python manage.py createsuperuser` with the same environment.

In a frontend terminal, from the root:

```bash
eval "$(fnm env --shell bash)"
fnm install
fnm use
cd frontend
npm install
npm run dev
```

Use `--shell zsh` for Zsh. `fnm install` is only needed when the pinned version is
missing. Open <http://127.0.0.1:5173>. Vite proxies `/api` to Django on port 8000.
Node selection affects this shell only; npm packages are installed locally.
`package-lock.json` is tracked.

Stop Django and Vite with Ctrl-C. Stop the database from the root:

```bash
docker compose down
```

Data is preserved. Do not add `-v` unless you intend to delete the database volume.

## Checks

With PostgreSQL running and `.env` exported, from the root:

```bash
export UV_PROJECT_ENVIRONMENT="$(pyenv prefix)"
cd backend
uv run pytest
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py migrate --check
```

Tests use a separate PostgreSQL test database; the Compose role can create it.
Tests cover health JSON, Admin availability and custom User persistence.
Generate future migrations with `uv run python manage.py makemigrations`, inspect
them, then apply with `uv run python manage.py migrate`.

With fnm-selected Node, from `frontend/`:

```bash
npm test
npm run build
```

The frontend test renders the landing page. The build checks TypeScript and
creates production assets. No separate linter or formatter is configured.

## Structure and scope

- `backend/config/`: Django settings, routing, ASGI and WSGI entry points.
- `backend/grinder/`: custom User, Admin, health API, migrations and tests.
- `frontend/src/pages/`: landing page; `components/`, `api/`, `domain/`, and
  `platform/` reserve space for future implementation.
- `docs/product.md`, `docs/architecture.md`, `docs/ux/main-screen.md`: source of
  truth for product, architecture and UX decisions.

Areas, Projects, Actions, timers, reports, authentication UI and mobile-platform
integrations are deferred to later issues.
