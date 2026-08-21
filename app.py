from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import products, orders, user

from services.reminders import (
    start_scheduler,
    stop_scheduler,
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(products.router)
app.include_router(orders.router)
app.include_router(user.router)


@app.on_event("startup")
def startup_event():
    start_scheduler()


@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()