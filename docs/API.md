# API reference (v1)

Base URL: `{origin}/api/` (e.g. `http://127.0.0.1:8000/api/`)

## Auth

| Method | Path | Body | Auth |
|--------|------|------|------|
| POST | `auth/register/` | `email`, `username`, `password`, `phone_number?` | No |
| POST | `auth/login/` | `email`, `password` | No |
| POST | `auth/refresh/` | `refresh` | No |
| GET/PATCH | `auth/profile/` | — / profile fields | Bearer |
| POST | `auth/password/reset/` | `email` | No |
| POST | `auth/password/reset/confirm/` | `uid`, `token`, `new_password` | No |

## Login response

```json
{ "access": "<jwt>", "refresh": "<jwt>" }
```

## Refresh response

```json
{ "access": "<jwt>" }
```

## Health

`GET /api/health/` → `{ "status": "ok", "service": "myapp_backend" }`
