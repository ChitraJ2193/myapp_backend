from decouple import config  # noqa: E402

from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

if config("CORS_ALLOW_ALL", default=False, cast=bool):
    CORS_ALLOW_ALL_ORIGINS = True

# Optional: run/tests without Docker (pytest, quick start)
if config("USE_SQLITE", default=False, cast=bool):
    DATABASES["default"] = {  # noqa: F405
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
