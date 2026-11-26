from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.webhook_endpoint import WebhookEndpointCreate, WebhookEndpointResponse
from app.services.webhook_endpoint_service import create_endpoint, get_endpoints
from app.models import WebhookEndpoint
from app.schemas.webhook_request import WebhookRequestResponse
from app.services.webhook_request_service import get_endpoint_requests, get_webhook_request

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

@router.get("/{endpoint_id}/requests", response_model = list[WebhookRequestResponse])
async def list_endpoint_requests(endpoint_id: UUID, method: str | None = Query(default = None), date_from: datetime | None = Query(default = None), date_to: datetime | None = Query(default = None), search: str | None = Query(default = None), skip: int = Query(default = 0, ge = 0), limit: int = Query(default = 50, ge = 1, le = 100), db: AsyncSession = Depends(get_db)):
    endpoint = await db.get(WebhookEndpoint, endpoint_id)

    if not endpoint:
        raise HTTPException(status_code = 404, detail = "Endpoint not found")

    return await get_endpoint_requests(db, endpoint_id, skip, limit, method, date_from, date_to, search)

@router.get("/{endpoint_id}/requests/{request_id}", response_model = WebhookRequestResponse)
async def get_request_detail(endpoint_id: UUID, request_id: UUID, db: AsyncSession = Depends(get_db)):
    request = await get_webhook_request(db, endpoint_id, request_id)

    if not request:
        raise HTTPException(status_code = 404, detail = "Webhook request not found")

    return request