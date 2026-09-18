# Time Grinder — Architecture

## Status

Version: 0.2

This document describes the initial architecture for the Time Grinder MVP.

The architecture should optimize for:

- fast MVP development;
- mobile-first UX;
- clear separation between frontend and backend;
- ability to reuse the frontend across Web, Telegram Mini App and iOS;
- simple deployment;
- ability to evolve without a major rewrite.


# High-level architecture

Time Grinder consists of:

- a React frontend;
- a Django + Django Ninja backend;
- a PostgreSQL database.

The frontend and backend are separate applications but live in the same repository.

```text
             ┌──────────────────────┐
             │      React UI        │
             │ TypeScript + Vite    │
             └──────────┬───────────┘
                        │
                 platform layer
            ┌───────────┼────────────┐
            │           │            │
            ▼           ▼            ▼
           Web       Telegram     Capacitor
                                      │
                                      ▼
                                     iOS

                        │
                        │ HTTPS / JSON
                        ▼

             ┌──────────────────────┐
             │    Django Ninja      │
             │   Django + Python    │
             └──────────┬───────────┘
                        │
                   Django ORM
                        │
                        ▼
                   PostgreSQL
```

The backend is the source of truth for persisted application data.


# Repository structure

Time Grinder uses a monorepo.

Initial structure:

```text
time_grinder/
├── frontend/
├── backend/
├── docs/
│   ├── product.md
│   ├── architecture.md
│   └── ux/
│       └── main-screen.md
├── docker-compose.yml
├── AGENTS.md
├── README.md
└── .gitignore
```


# Frontend

## Technology

The frontend uses:

- React
- TypeScript
- Vite

The application is mobile-first.

The frontend should not depend on Next.js or another server-side rendering framework.

Server-side application logic lives in Django.


## Frontend responsibilities

The frontend is responsible for:

- rendering the user interface;
- interaction and gesture handling;
- displaying timer state;
- drag-and-drop time entry;
- optimistic UI where appropriate;
- calling the backend API;
- handling platform-specific capabilities through adapters.


## Platform independence

Most frontend code should not know which platform it is running on.

Platform-specific behavior should be isolated behind a small abstraction layer.

Conceptual structure:

```text
frontend/src/
├── pages/
├── components/
├── api/
├── domain/
└── platform/
    ├── web.ts
    ├── telegram.ts
    └── capacitor.ts
```

Platform adapters may provide capabilities such as:

- haptic feedback;
- platform initialization;
- theme information;
- viewport / safe-area information;
- authentication information;
- native notifications;
- platform-specific lifecycle events.

Application components should depend on platform interfaces rather than directly importing Telegram or Capacitor APIs wherever practical.

Only the web adapter needs to be implemented for the first MVP. Telegram and Capacitor adapters should be introduced when those platforms are actually integrated.


## Platform targets

### Web

The first implementation target is a normal browser application.

```text
React + Vite
    ↓
Browser
    ↓
Django Ninja
```


### Telegram Mini App

Telegram is a possible future frontend host.

The same React application should be reusable as a Telegram Mini App.

Telegram-specific behavior should remain inside the platform adapter.

Possible platform-specific capabilities include:

- Telegram authentication;
- theme;
- viewport;
- safe areas;
- haptics.

Telegram support is not required for the initial MVP.


### iOS

The planned iOS distribution mechanism is Capacitor.

```text
React + Vite
    ↓
Capacitor
    ↓
Xcode
    ↓
iPhone / TestFlight / App Store
```

The goal is to reuse the same frontend codebase rather than create a separate mobile frontend.

Capacitor may later provide access to native capabilities such as:

- haptics;
- notifications;
- filesystem;
- application lifecycle events.

Capacitor integration is not required for the first web MVP, but the frontend architecture must not prevent it.


# Backend

## Technology

The backend uses:

- Python
- Django
- Django Ninja
- Django ORM
- PostgreSQL

Database schema changes use Django migrations.

Python dependencies are managed with `uv`.

Backend tests use:

- pytest
- pytest-django


## Backend responsibilities

The backend is responsible for:

- persistence;
- domain rules;
- data validation;
- user data isolation;
- timer state;
- reports and aggregations;
- enforcing invariants;
- providing the API used by all client platforms.


## API style

The frontend communicates with Django Ninja using HTTPS and JSON.

The MVP uses REST.

GraphQL is not required.

WebSockets are not required.

The frontend must not communicate directly with PostgreSQL.


# Domain model

The core hierarchy is:

```text
User
  ↓
Area
  ↓
Project
  ↓
Action
```


## User

A User owns their Time Grinder data.

The data model must support multiple users from the beginning.

Full authentication and account management are not part of the MVP.

The initial application may operate as a predefined development/default user.

A custom Django User model should be defined from the beginning to avoid changing the user model after migrations and persisted data already exist.

Conceptual fields:

```text
User
----
id
username / identity fields
name
timezone
created_at
updated_at
```

`timezone` uses an IANA timezone identifier.

Example:

```text
Europe/Nicosia
```

The custom User model may extend Django's `AbstractUser`.


## Area

An Area represents a broad part of life.

Examples:

- Health
- Self Improvement
- Family
- Adulting
- Recreation

Areas are predefined in the MVP.

Conceptual fields:

```text
Area
----
id
user_id
name
created_at
updated_at
```


## Project

A Project represents a concrete activity or responsibility inside an Area.

Examples:

```text
Health
├── Sport
└── Sleep

Family
├── Baby
└── Wife Time

Adulting
├── Work
└── Chores

Recreation
├── Games
└── Chill

Self Improvement
├── Write Games
└── Write Programs
```

Projects are predefined in the MVP.

Conceptual fields:

```text
Project
-------
id
user_id
area_id
name
created_at
updated_at
```


## Action

An Action represents one fact of spending time on a Project.

Time is the primary information stored by an Action.

Description is optional.

Actions may be created in two ways:

- by running a timer;
- by manually adding a duration.

Conceptual fields:

```text
Action
------
id
user_id
project_id

started_at          nullable
ended_at            nullable
duration_seconds    nullable

description         nullable

created_at
updated_at
```


# Action semantics

## Manual Action

A manually added Action represents a duration without claiming that the exact historical start and end time are known.

Example:

The user drags `+30m` onto `Baby`.

```text
project_id = Baby
started_at = NULL
ended_at = NULL
duration_seconds = 1800
```

This reflects the product's approximate time-tracking philosophy.


## Running timer

A running timer is represented as an unfinished Action.

Example:

```text
project_id = Work
started_at = 2026-09-17T15:00:00Z
ended_at = NULL
duration_seconds = NULL
```

There is no separate `RunningTimer` domain entity.


## Completed timer

When Stop is pressed:

```text
ended_at = current UTC time
duration_seconds = ended_at - started_at
```

The Action becomes a normal completed Action.


## Timer invariant

A User may have at most one running Action at a time.

A running Action is defined as:

```text
started_at IS NOT NULL
AND ended_at IS NULL
```

This invariant must be enforced by the backend and, where practical, by the database.

With PostgreSQL and Django ORM, a conditional unique constraint should be used where practical so the database also protects this invariant.

Conceptually:

```python
UniqueConstraint(
    fields=["user"],
    condition=Q(
        started_at__isnull=False,
        ended_at__isnull=True,
    ),
    name="one_running_action_per_user",
)
```


# Timer architecture

The timer does not depend on a JavaScript counter as the source of truth.

The backend stores the timer's `started_at` timestamp.

The frontend calculates the displayed elapsed time as:

```text
current_time - started_at
```

The UI may update this display every second locally.

No API request is required every second.

This means the timer survives:

- browser refresh;
- closing and reopening the app;
- iOS application suspension;
- temporary frontend interruption.

Starting and stopping the timer require backend requests.

Running the visible timer does not.


# Time and timezone handling

All persisted timestamps are stored in UTC.

User-facing day boundaries are calculated using the User's configured timezone.

For example, the `Today` report represents the user's local calendar day, not the server's UTC day.

The frontend may display local times, but UTC remains the persistence format.


# Undo

Undo is intentionally simple in the MVP.

Undo reverses the most recent time-recording operation.

Examples:

- manual `+15m`;
- manual `+30m`;
- manual `+1h`;
- completed timer Action.

The client should call an explicit backend Undo operation rather than attempting to reconstruct domain behavior locally.

Conceptually:

```text
POST /api/undo
```

For the MVP, the backend may implement Undo by deleting the most recently created eligible Action.

A more sophisticated event/history model is explicitly not required.


# Initial API

The exact schemas may evolve during implementation, but the initial API shape is expected to resemble:

```text
GET    /api/projects

GET    /api/actions
POST   /api/actions
PATCH  /api/actions/{id}
DELETE /api/actions/{id}

POST   /api/timer/start
POST   /api/timer/stop
GET    /api/timer

POST   /api/undo

GET    /api/reports/today
```

The API expresses product operations rather than exposing database tables directly.

For example, the frontend uses `/api/timer/start` instead of creating a partially populated Action itself.


# Reports

The first report is time spent by Project for Today.

Conceptually:

```text
GET /api/reports/today
```

The response should provide enough information to render totals on the main screen.

Example:

```json
{
  "projects": [
    {
      "project_id": 1,
      "duration_seconds": 8100
    },
    {
      "project_id": 2,
      "duration_seconds": 3600
    }
  ]
}
```

The backend owns aggregation logic.

The frontend should not need to download all historical Actions merely to calculate project totals.


# Frontend state

Frontend state should be kept simple.

The frontend needs state for at least:

- Projects;
- Today totals;
- current running timer;
- recent Actions where required;
- UI interaction state.

The backend remains the source of truth.

A frontend state-management library should not be introduced until the application complexity justifies it.

React state and small focused abstractions are preferred initially.

A dedicated `store/` directory should not be created until there is a concrete need for shared application state across multiple parts of the UI.


# Persistence and optimistic UI

Fast interactions are important to the product.

For operations such as dropping a time bubble onto a Project, the UI may update optimistically.

However:

- failed writes must be visible to the user;
- the UI must recover from failed persistence;
- data loss must never be silent.

The backend remains authoritative.


# Django Admin

Django Admin may be used as an internal development and operational tool.

It is not part of the Time Grinder end-user product UI.

For the MVP it may be used to:

- inspect Users;
- inspect Actions;
- manage predefined Areas;
- manage predefined Projects;
- diagnose persisted data.

A custom end-user Area/Project editor is not required for the MVP.


# Development environment

Local development should remain simple.

Recommended setup:

```text
Frontend
React/Vite
→ npm run dev

Backend
Django + Django Ninja
→ uv run python manage.py runserver

Database
PostgreSQL
→ Docker Compose
```

Frontend and backend do not need to run inside Docker during normal local development.

PostgreSQL should run via Docker Compose initially.

The scaffold uses Python 3.12.8 in the dedicated pyenv virtualenv
`3.12.8_time_grinder`. Set `UV_PROJECT_ENVIRONMENT` to the output of `pyenv prefix`
so uv installs and runs dependencies in that environment. This explicit local
setup choice replaces the repository-local `.venv`. Node is selected through
fnm using the root `.node-version`; npm dependencies stay in frontend/node_modules.

The scaffold exposes only `GET /api/health`, Django Admin, and a static React
landing page. The custom User extends AbstractUser without additional fields;
timezone preferences and domain operations are deferred. Vite proxies `/api`
to Django during development.


# Backend project structure

Initial direction:

```text
backend/
├── pyproject.toml
├── uv.lock
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── grinder/
    ├── __init__.py
    ├── apps.py
    ├── models.py
    ├── api.py
    ├── schemas.py
    ├── services.py
    ├── admin.py
    ├── migrations/
    └── tests/
```

The MVP should begin with one primary Django domain app, `grinder`.

Do not split the backend into separate Django apps for Users, Areas, Projects, Actions and Reports until the domain has enough complexity to justify those boundaries.

Exact internal boundaries should remain pragmatic.

Layers should only be introduced when they have a clear responsibility.

Avoid unnecessary enterprise abstractions.


# Frontend project structure

Initial direction:

```text
frontend/
├── package.json
├── package-lock.json
├── vite.config.ts
└── src/
    ├── pages/
    ├── components/
    ├── api/
    ├── domain/
    ├── platform/
    └── main.tsx
```

This structure may evolve as real implementation requirements become clear.


# Testing

## Backend

Use:

```text
pytest
pytest-django
```

Important backend behavior should be tested, especially:

- only one running timer per user;
- timer start / stop;
- manual Action creation;
- Undo;
- Today aggregation;
- user data isolation.


## Frontend

Use:

- Vitest
- React Testing Library

Focus frontend tests on important behavior rather than implementation details.


## End-to-end testing

An E2E framework is not required initially.

Playwright may be added once the main workflow stabilizes.


# Deployment

The application should be deployable using containers.

The initial infrastructure target is AWS.

Exact AWS services are deliberately not fixed in this architecture document.

The initial production topology may be approximately:

```text
Internet
   │
   ▼
HTTPS / reverse proxy
   │
   ├── /      → frontend
   │
   └── /api   → Django Ninja
                    │
                    ▼
                PostgreSQL
```

The first deployment may use a single small server.

More complex infrastructure such as Kubernetes, Redis, queues, autoscaling or separate managed services is not required for the MVP.

Deployment-specific decisions should eventually live in:

```text
docs/deployment.md
```


# Authentication

The domain model supports multiple Users from the beginning.

Real authentication is intentionally deferred.

For the first MVP/dev version:

- a predefined user may be used;
- API requests may operate under that user;
- user IDs must still exist in persisted data.

Later authentication may come from:

- normal web authentication;
- Telegram;
- iOS/web identity providers.

The domain model should not depend on a specific authentication provider.


# Explicit non-goals

The architecture does not currently require:

- GraphQL;
- WebSockets;
- Redis;
- message queues;
- Kubernetes;
- microservices;
- event sourcing;
- complex CQRS;
- separate frontend repositories per platform;
- a native Swift frontend;
- a separate React Native frontend;
- offline synchronization;
- push notifications;
- server-side React rendering;
- SQLAlchemy;
- Alembic.


# Architectural principles

1. Keep the frontend and backend clearly separated.
2. Keep platform-specific frontend code isolated.
3. Keep PostgreSQL behind the Django backend.
4. Make the backend the source of truth.
5. Reuse one frontend across platforms where practical.
6. Store timestamps in UTC.
7. Prefer simple domain concepts over infrastructure abstractions.
8. Do not introduce systems needed only for hypothetical scale.
9. Optimize the MVP for fast iteration.
10. Preserve an evolutionary path toward real multi-user web and mobile apps.
