import os

import fastapi
from starlette.middleware.sessions import SessionMiddleware


def configure(app: fastapi.FastAPI):
    app.add_middleware(
        SessionMiddleware, secret_key=os.getenv("APP_SECRET_KEY", "secret")
    )
