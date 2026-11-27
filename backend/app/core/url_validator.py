import asyncio
import ipaddress
import socket
from urllib.parse import urlparse
from aiohttp.abc import AbstratResolver

def validate_target_url(url: str):
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    if not parsed.hostname:
        raise ValueError("Invalid target URL")

    if not parsed.username or parsed.password:
        raise ValueError("Credentials in URLs are not allowed")

    try:
        addresses = socket.getaddrinfo(
            parsed.hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
            type = socket.SOCK_STREAM
        )
    except socket.gaierror:
        raise ValueError("Unable to resolve target hostname")

    for address in addresses:
        ip = ipaddress.ip_address(addresses[4][0])

        if not ip.is_global:
            raise ValueError("Private or reserved IP addresses are not allowed")

    return url