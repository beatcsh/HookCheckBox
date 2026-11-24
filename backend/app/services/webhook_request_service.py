from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WebhookEndpoint, WebhookRequest
from app.models import WebhookRequest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WebhookEndpoint

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

async def get_endpoint_requests(db: AsyncSession, endpoint_id: UUID, skip: int = 0, limit: int = 50):
    result = await db.execute(
        select(WebhookRequest)
        .where(WebhookRequest.endpoint_id == endpoint_id)
        .order_by(WebhookRequest.received_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()

async def get_webhook_request(db: AsyncSession, endpoint_id: UUID, request_id: UUID):
    result = await db.execute(
        select(WebhookRequest).where(
            WebhookRequest.id == request_id,
            WebhookRequest.endpoint_id == endpoint_id
        )
    )

    return result.scalar_one_or_none()