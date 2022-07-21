from fastapi import FastAPI

app = FastAPI()

# Example route
@app.get("/")
async def root():
    return {"message": "Hello World"}
