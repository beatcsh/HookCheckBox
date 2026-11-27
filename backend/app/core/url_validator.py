import asyncio
import ipaddress
import socket
from urllib.parse import urlparse
from aiohttp.abc import AbstractResolver

def validate_target_url(url: str):
    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are allowed")

    if not parsed.hostname:
        raise ValueError("Invalid target URL")

    if parsed.username is not None or parsed.password is not None:
        raise ValueError("Credentials in URLs are not allowed")

    try:
        parsed.port
    except ValueError:
        raise ValueError("Invalid target port")

    return url

class SafeResolver(AbstractResolver):
    async def resolve(self, host, port = 0, family = socket.AF_UNSPEC):
        loop = asyncio.get_running_loop()

        try:
            addresses = await loop.getaddrinfo(
                host,
                port,
                family = family,
                type = socket.SOCK_STREAM
            )
        except socket.gaierror:
            raise OSError("Unable to resolve target hostname")

        validated = []
        seen = set()

        for af, socktype, proto, canonname, sockaddr in addresses:
            ip = ipaddress.ip_address(sockaddr[0])

            if not ip.is_global:
                raise OSError("Private or reserved IP addresses are not allowed")

            if ip.compressed in seen:
                continue

            seen.add(ip.compressed)

            validated.append({
                "hostname": host,
                "host": ip.compressed,
                "port": port,
                "family": af,
                "proto": proto,
                "flags": 0
            })

        if not validated:
            raise OSError("No valid public IP address found")
        
        return validated

    async def close(self):
        pass