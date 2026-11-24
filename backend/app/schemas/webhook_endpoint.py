from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class WebhookEndpointCreate(BaseModel):
    name: str

class WebhookEndpointResponse(BaseModel):
    id: UUID
    name: str
    token: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)