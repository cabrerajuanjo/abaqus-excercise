from config.env import env

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOW_METHODS = (
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# )

BASE_BACKEND_URL = env.str("DJANGO_BASE_BACKEND_URL", default="http://localhost:8000")
BASE_FRONTEND_URL = env.str("DJANGO_BASE_FRONTEND_URL", default="http://localhost:5173")
CORS_ORIGIN_WHITELIST = env.list("DJANGO_CORS_ORIGIN_WHITELIST", default=[BASE_FRONTEND_URL])

