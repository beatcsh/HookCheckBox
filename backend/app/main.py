from fastapi import FastAPI
from app.api.endpoints import router as endpoints_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "HookCheckBox",
    description = "Webhook Inspector and Debugging Tool",
    version = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [ "http://localhost:5173" ],
    allow_credentials = True,
    allow_methods = [ "*" ],
    allow_headers = [ "*" ],
)

app.include_router(
    endpoints_router,
    prefix = "/api/v1"
)

@app.get("/")
async def root():
    return { "message": "HookCheckBox API is running" }