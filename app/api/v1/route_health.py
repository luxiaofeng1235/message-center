from fastapi import APIRouter, Request
import platform
import socket

from app.core.response import success

router = APIRouter()


@router.get("/health")
async def health(request: Request):
    os_info = platform.platform()
    host_ip = None
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        host_ip = None
    client_ip = request.client.host if request.client else None
    return success({"status": "ok", "os": os_info, "ip": client_ip or host_ip})
