from fastapi import FastAPI
from app.api.endpoints import router as endpoints_router
from app.api.hooks import router as hooks_router
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

app.include_router(
    hooks_router,
    prefix = "/api/v1"
)

@app.get("/")
async def root():
    return { "message": "HookCheckBox API is running" }


"""
$token = "Xdyh9Ra5zC6m4Gaw4utfWYvu4zg2dzzdLvF6mW1NgCw"

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/hooks/$token?source=test" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"event":"user.created","user":{"id":15,"name":"Beat"}}'

"""