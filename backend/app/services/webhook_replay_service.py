import asyncio
import aiohttp
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.webhook_request_service import get_webhook_request
from app.core.url_validator import validate_target_url, SafeResolver

async def replay_webhook(db: AsyncSession, endpoint_id: UUID, request_id: UUID, target_url: str):
    
    original_request = await get_webhook_request(
        db = db,
        endpoint_id = endpoint_id,
        request_id = request_id
    )

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

    print(repr(target_url))

    validate_target_url(target_url)

    timeout = aiohttp.ClientTimeout(total = 15)

    connector = aiohttp.TCPConnector(
        resolver = SafeResolver(),
        use_dns_cache = False
    )

    try:
        async with aiohttp.ClientSession(
            connector = connector,
            timeout = timeout,
            trust_env = False
        ) as client:
            async with client.request(
                method = original_request.method,
                url = target_url,
                headers = headers,
                data = original_request.body,
                allow_redirects = False
            ) as response:
                return {
                    "status_code": response.status,
                    "response_body": await response.text(errors = "replace"),
                    "response_headers": dict(response.headers)
                }
    
    except asyncio.TimeoutError:
        raise ValueError("The target server took too long to respond")
    
    except aiohttp.ClientError:
        raise ValueError("Unable to connect to the target server")