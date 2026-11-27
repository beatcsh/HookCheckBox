import httpx
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.webhook_request_service import get_webhook_request
from app.core.url_validator import validate_target_url

async def replay_webhook(db: AsyncSession, endpoint_id: UUID, request_id: UUID, target_url: str):
    original_request = await get_webhook_request(
        db = db,
        endpoint_id = endpoint_id,
        request_id = request_id
    )

    try:
        validate_target_url(target_url)
    except ValueError as error:
        raise ValueError(str(error))

    if not original_request:
        return None

    headers = dict(original_request.headers or {})

    excluded_headers = {
        "host",
        "content-length",
        "connection",
        "transfer-encoding"
    }

    headers = {
        key: value
        for key, value in headers.items()
        if key.lower() not in excluded_headers
    }

    try:
        async with httpx.AsyncClient(
            timeout = 15.0,
            follow_redirects = False
        ) as client:
            response = await client.request(
                method = original_request.method,
                url = target_url,
                headers = headers,
                content = original_request.body
            )
    
    except httpx.TimeoutException:
        raise ValueError("The target server took too long to respond")
    
    except httpx.RequestError:
        raise ValueError("Unable to connect to the target server")
    
    return {
        "status_code": response.status_code,
        "response_body": response.text,
        "response_headers": dict(response.headers)
    }