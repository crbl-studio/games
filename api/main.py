from fastapi import FastAPI
from src.routes import auth

app = FastAPI()

app.include_router(auth.router)
