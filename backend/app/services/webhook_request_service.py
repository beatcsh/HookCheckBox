from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WebhookEndpoint, WebhookRequest

async def save_webhook_request(db: AsyncSession, endpoint: WebhookEndpoint, method: str, headers: dict, query_params: dict, body: str | None, content_type: str | None):
    webhook_request = WebhookRequest(
        endpoint_id = endpoint.id,
        method = method,
        headers = headers,
        query_params = query_params,
        body = body,
        content_type = content_type
    )

    db.add(webhook_request)
    await db.commit()
    await db.refresh(webhook_request)

    return webhook_request