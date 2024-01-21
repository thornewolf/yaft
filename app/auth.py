from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from fastapi import Query
from starlette.config import Config

config = Config("../.env")
oauth = OAuth(config)
auth0 = oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)
assert auth0

router = APIRouter(prefix="", tags=["authentication"])


@router.get("/login")
async def login(request: Request, next: str = Query(None)):
    next_url = next or str(request.url_for("index"))
    redirect_uri = str(request.url_for("callback")) + "?next=" + next_url
    print(f"login redirect_uri: {redirect_uri}")
    return await auth0.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def callback(request: Request, next: str = Query(None)):
    jwt = await auth0.authorize_access_token(request)
    request.session["user"] = jwt
    # optionally store user here
    next = next or str(request.url_for("index"))
    return RedirectResponse(next)


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    index_url = str(request.url_for("index"))
    logout_url = (
        "https://"
        + env.get("AUTH0_DOMAIN", "")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": index_url,
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
    return RedirectResponse(url=logout_url)


def configure(app):
    app.include_router(router)
