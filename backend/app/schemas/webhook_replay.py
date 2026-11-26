from pydantic import BaseModel, HttpUrl

class WebhookReplayCreate(BaseModel):
    target_url: HttpUrl