from pydantic import BaseModel, HttpUrl

class WebhookReplayCreate(BaseModel):
    target_url: HttpUrl

class WebhookReplayResponse(BaseModel):
    status_code: int
    response_body: str
    response_headers: dict[str, str]