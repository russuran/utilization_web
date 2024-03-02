from typing import Union
import secrets
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Response, Depends
import starlette.status as status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from crud import get_items
from database import SessionLocal, engine

import ast

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/send')
async def get_from_form(request: Request, name: str = Form(...), tel: str = Form(...), city: str = Form(...), story: str = Form(...)):
    print(name, city, story, tel)
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@app.post('/add-to-cart')
async def get_add_val(response: Response, request: Request, val: str = Form(...), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = ast.literal_eval(request.cookies["product_ids_in_cart"])
    data.append(int(val))

    if "choosen" not in request.cookies.keys() or "product_ids_in_cart" not in request.cookies.keys():
        response = RedirectResponse("/#openModal-catalog", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="product_ids_in_cart", value=data)

        return response
    
    response = RedirectResponse("/#openModal-catalog", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="product_ids_in_cart", value=data)

    return response


@app.post('/del-from-cart')
async def get_add_val(response: Response, request: Request, val: str = Form(...), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = ast.literal_eval(request.cookies["product_ids_in_cart"])
    del data[data.index(int(val))]

    if "choosen" not in request.cookies.keys() or "product_ids_in_cart" not in request.cookies.keys():
        response = RedirectResponse("/#openModal-catalog", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="product_ids_in_cart", value=data)

        return response
    
    response = RedirectResponse("/#openModal-catalog", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="product_ids_in_cart", value=data)

    return response


@app.post('/del-from-cart-in-cart')
async def get_add_val(response: Response, request: Request, val: str = Form(...), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = ast.literal_eval(request.cookies["product_ids_in_cart"])
    del data[data.index(int(val))]

    if "product_ids_in_cart" not in request.cookies:
        response = RedirectResponse("/cart", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="product_ids_in_cart", value=data)

        return response
    
    response = RedirectResponse("/cart", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="product_ids_in_cart", value=data)

    return response


@app.get("/")
async def mainpage(response: Response, request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    if "product_ids_in_cart" not in request.cookies:
        response = templates.TemplateResponse("index.html", {"request": request, "items": items, "data": []}) 
        response.set_cookie(key="product_ids_in_cart", value=[])
        return response

    
    data = ast.literal_eval(request.cookies["product_ids_in_cart"])

    return templates.TemplateResponse("index.html", {"request": request, "items": items, "data": data})


@app.get("/cart")
async def mainpage(response: Response, request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    
    if "product_ids_in_cart" not in request.cookies:
        response = templates.TemplateResponse("cart.html", {"request": request, "data": ast.literal_eval(request.cookies["product_ids_in_cart"]), "items": data}) 
        response.set_cookie(key="product_ids_in_cart", value=[])
        return response
    
    goods = ast.literal_eval(request.cookies["product_ids_in_cart"])
    items_db = get_items(db, skip=skip, limit=limit)
    data = []
    for i in goods:
        for j in items_db:
            if i == j[0]:
                data.append(j)
    return templates.TemplateResponse("cart.html", {"request": request, "data": ast.literal_eval(request.cookies["product_ids_in_cart"]), "items": data})


@app.get("/test")
async def test(request: Request):
    return request.cookies



