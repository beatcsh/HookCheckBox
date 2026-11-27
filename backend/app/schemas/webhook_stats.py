from datetime import datetime
from pydantic import BaseModel

class WebhookEndpointStatsResponse(BaseModel):
    total_requests: int
    requests_today: int
    last_received_at: datetime | None
    requests_by_method: dict[str, int]