from uuid import UUID
from app.models import WebhookRequest
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.models import WebhookEndpoint
from app.services.webhook_request_service import save_webhook_request

router = APIRouter(prefix = "/hooks", tags = [ "Webhooks" ])

@router.api_route("/{token}", methods = [ "GET", "POST", "PUT", "PATCH", "DELETE" ])
async def receive_webhook(token: str, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(WebhookEndpoint).where(WebhookEndpoint.token == token)
    )

    endpoint = result.scalar_one_or_none()

    if not endpoint or not endpoint.is_active:
        raise HTTPException(status_code = 404, detail = "Webhook endpoint not found")

    body = await request.body()

    await save_webhook_request(
        db = db,
        endpoint = endpoint,
        method = request.method,
        headers = dict(request.headers),
        query_params = dict(request.query_params),
        body = body.decode("utf-8", errors = "replace") if body else None,
        content_type = request.headers.get("content-type")
    )