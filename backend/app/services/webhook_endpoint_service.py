import secrets
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import WebhookEndpoint

async def create_endpoint(db: AsyncSession, name: str):
    endpoint = WebhookEndpoint(
        name = name,
        token = secrets.token_urlsafe(32)
    )

    db.add(endpoint)
    await db.commit()
    await db.refresh(endpoint)

    return endpoint

async def get_endpoints(db: AsyncSession):
    result = await db.execute(
        select(WebhookEndpoint).order_by(
            WebhookEndpoint.created_at.desc()
        )
    )

    return result.scalars().all()