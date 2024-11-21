
# ----- Compraventa el poblado --------
from fastapi import FastAPI, Body, status, Response, HTTPException  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from routers import products, users


app = FastAPI()
app.title = 'Compraventa el Poblado'

app.include_router(products.router)
app.include_router(users.router)
