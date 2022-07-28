from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from src.routes import auth

app = FastAPI()

app.include_router(auth.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
