from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.webhook_endpoint import WebhookEndpointCreate, WebhookEndpointResponse
from app.services.webhook_endpoint_service import create_endpoint, get_endpoints

router = APIRouter(
    prefix = "/endpoints", 
    tags = ["Endpoints"]
)

@router.post("/add", response_model = WebhookEndpointResponse, status_code = 201)
async def create(data: WebhookEndpointCreate, db: AsyncSession = Depends(get_db)):
    return await create_endpoint(db, data.name)

@router.get("/get", response_model = list[WebhookEndpointResponse])
async def list_all(db: AsyncSession = Depends(get_db)):
    return await get_endpoints(db)