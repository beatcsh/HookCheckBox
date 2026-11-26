from uuid import UUID
from datetime import datetime
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

async def get_webhook_request(db: AsyncSession, endpoint_id: UUID, request_id: UUID):
    result = await db.execute(
        select(WebhookRequest).where(
            WebhookRequest.id == request_id,
            WebhookRequest.endpoint_id == endpoint_id
        )
    )

    return result.scalar_one_or_none()

async def get_endpoint_requests(db: AsyncSession, endpoint_id: UUID, skip: int = 0, limit: int = 0, method: str | None = None, date_from: datetime | None = None, date_to: datetime | None = None, search: str | None = None):
    query = select(WebhookRequest).where(
        WebhookRequest.endpoint_id == endpoint_id
    )

    if method:
        query = query.where(WebhookRequest.method == method.upper())

    if date_from:
        query = query.where(WebhookRequest.date_from == date_from.upper())

    if date_to:
        query = query.where(WebhookRequest.date_to == date_to.upper())

    if search:
        query = query.where(WebhookRequest.body.ilike(f"%{search}%"))

    query = (
        query
        .order_by(WebhookRequest.received_at.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(query)

    return result.scalars().all()