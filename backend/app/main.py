from fastapi import FastAPI

app = FastAPI(
    title = "HookCheckBox",
    description = "Webhook Inspector and Debugging Tool",
    version = "1.0.0"
)

@app.get("/")
async def root():
    return { "message": "HookCheckBox API is running" }