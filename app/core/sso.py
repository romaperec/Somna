from fastapi_sso import GoogleSSO

from app.core.config import settings

google_sso = GoogleSSO(
    client_id=settings.google_sso.client_id,
    client_secret=settings.google_sso.client_secret,
    redirect_uri=settings.google_sso.redirect_uri,
)
