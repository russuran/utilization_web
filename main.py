from typing import Union

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class FormData(BaseModel):
    name: str
    tel: str
    city: str
    info: str


@app.post('/send')
async def get_from_form(request: Request):
    form = await request.form()
    data = FormData.parse_obj(dict(form))
    print(data)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def main_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

