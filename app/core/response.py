from fastapi.responses import JSONResponse
from fastapi import status


def success(data=None, msg: str = "ok"):
    return {"code": 1, "msg": msg, "data": data}


def fail(msg: str = "error", code: int = 0, status_code: int = status.HTTP_400_BAD_REQUEST):
    return JSONResponse(status_code=status_code, content={"code": code, "msg": msg, "data": None})
