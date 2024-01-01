from contextlib import asynccontextmanager
from fastapi import (
    Depends,
    FastAPI,
    Request,
    Response,
)
from fastapi.responses import HTMLResponse
from sqlmodel import select

from . import auth, db, middleware, models
from .common import render


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    yield


app = FastAPI(servers=[{"url": "http://127.0.0.1:8000"}], lifespan=lifespan)
middleware.configure(app)
auth.configure(app)


@app.get("/")
def index(request: Request, session=Depends(db.get_session)) -> Response:
    return render("Index", request=request, title="Home")


@app.get("/app")
def app_page(request: Request, session=Depends(db.get_session)) -> Response:
    return render("App", request=request, title="Home")


@app.get("/users")
def users(request: Request, session=Depends(db.get_session)) -> Response:
    statement = select(models.User)
    users = session.exec(statement).all()
    print(users)
    return render("Users", request=request, title="Users", users=users)
