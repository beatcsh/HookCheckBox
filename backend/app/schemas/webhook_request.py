from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class WebhookRequestResponse(BaseModel):
    id: UUID
    endpoint_id: UUID
    method: str
    headers: dict
    query_params: dict
    body: str | None
    content_type: str | None
    received_at: datetime

    model_config = ConfigDict(from_attributes = True)