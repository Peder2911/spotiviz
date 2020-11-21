import os

from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
import requests

from jinja2 import Environment,FileSystemLoader,select_autoescape

from config import *

HERE = os.path.abspath(os.path.split(__file__)[0])

app = FastAPI()

if PRODUCTION:
    app.add_middleware(GZipMiddleware, minimum_size=1000)

env = Environment(
        loader = FileSystemLoader(os.path.join(HERE,"templates")),
        autoescape = select_autoescape(["html","xml"])
    )

if PRODUCTION:
    app.mount("/static", StaticFiles(directory="static"), name = "static")
else:
    @app.get("/static/{path:path}")
    async def static(path: str, response: Response):
        try:
            proxy = requests.get(os.path.join(FRONTEND_DEV_SERVER,path))
        except requests.exceptions.ConnectionError:
            response.status_code = 404
            return response
        else:
            response.body = proxy.content
            response.status_code = proxy.status_code
            response.media_type = proxy.headers["content-type"]
            return response

@app.get("/")
async def root():
    tpl = env.get_template("index.html")
    html = tpl.render()
    return HTMLResponse(html) 
