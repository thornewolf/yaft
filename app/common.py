import os

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinjax import Catalog


_TEMPLATES_DIR = "app/templates"
templates = Jinja2Templates(_TEMPLATES_DIR)
catalog = Catalog(jinja_env=templates.env)
catalog.add_folder(_TEMPLATES_DIR)
catalog.add_folder("app/templates/components")
catalog.jinja_env.globals["ENV"] = os.environ.get("ENV")
catalog.jinja_env.globals["ENABLE_TRACKING"] = os.environ.get("ENABLE_TRACKING")
catalog.jinja_env.globals["ENABLE_LIT"] = os.environ.get("ENABLE_LIT")


def render(*args, **kwargs):
    return HTMLResponse(catalog.render(*args, **kwargs))
