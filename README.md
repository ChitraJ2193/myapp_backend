# myapp_backend (Django 4.2)

Step **1.2** scaffold: REST API + JWT + PostgreSQL + Redis/Celery hooks + Docker Compose for local DB.

## Google Cloud (manual — avoids console “abuse” flags)

An AI assistant **cannot** create a GCP project, add **$300** credits, or link billing to your account. You do that in [Google Cloud Console](https://console.cloud.google.com/) with a normal browser session.

**Safe practice (automation-friendly):**

- Use **official APIs / gcloud** with a **service account** and **budget alerts**; do not run bots that drive the Console UI or mass-create resources.
- Keep **2FA** on the Google account; store keys in **Secret Manager**, not in chat or repos.
- For **Vertex AI / Gemini**: enable APIs in the project you own; usage is billed per product terms — it is separate from “Claude” subscriptions unless you explicitly integrate them.

## Quick start (local)

```bash
cd myapp_backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

**Database (Docker PostgreSQL):**

```bash
docker compose up -d
export DJANGO_SETTINGS_MODULE=myapp_backend.settings.dev
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Health:** `GET http://127.0.0.1:8000/api/health/`

**Auth (JWT):**

- `POST /api/auth/register/` — JSON: `email`, `username`, `password`
- `POST /api/auth/login/` — JSON: `email`, `password` → `access`, `refresh`
- `POST /api/auth/refresh/` — refresh token
- `GET|PATCH /api/auth/profile/` — authenticated user

## Settings modules

| Module | Use |
|--------|-----|
| `myapp_backend.settings.dev` | Local development |
| `myapp_backend.settings.staging` | Staging |
| `myapp_backend.settings.production` | Production |
| `myapp_backend.settings.test` | pytest (in-memory SQLite) |

## Celery

`CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` default to Redis. Start a worker after Redis is up:

```bash
celery -A myapp_backend worker -l info
```

## Tests

```bash
pytest
```

## Agent approval prompt (Step 1.2)

Confirm: dependency list, extra apps, PostgreSQL vs SQLite for dev, and whether Celery is required for the first milestone. After approval → database schema and feature work (Phase 2+).
