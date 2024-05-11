from os import path as os_path
from pathlib import Path


from environ.environ import Env as environment_singleton


from .constants import ONE_YEAR_IN_SECONDS


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG_SECRET_KEY = "cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag"
DEBUG_TOKEN_SALT = "NiqJ241x1B44tGj5mAYW"

env = environment_singleton(
    # set casting, default value
    SECRET_KEY=(str, DEBUG_SECRET_KEY),
    DEBUG=(bool, True),
    CSRF_COOKIE_SECURE=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    SECURE_SSL_REDIRECT=(bool, False),
    SECURE_HSTS_SECONDS=(int, ONE_YEAR_IN_SECONDS),
    SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, False),
    SECURE_HSTS_PRELOAD=(bool, False),
    SECURE_CONTENT_TYPE_NOSNIFF=(bool, False),
    JWT_VALIDITY_PERIOD_IN_DAYS=(float, 1),
    RT_VALIDITY_PERIOD_IN_DAYS=(float, 7),
    JWT_ENCRYPTION_ALGORITHM=(str, "HS256"),
    SAMESITE_COOKIE=(str, "Strict"),
    REFRESH_TOKEN_SALT=(str, DEBUG_TOKEN_SALT),
)

# Take environment variables from .env file
environment_singleton.read_env(os_path.join(BASE_DIR, ".env"))
