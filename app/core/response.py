from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel


def _serialize(data):
    if isinstance(data, BaseModel):
        return data.model_dump(mode="json")
    if isinstance(data, (list, tuple)):
        return [_serialize(item) for item in data]
    if isinstance(data, dict):
        return {k: _serialize(v) for k, v in data.items()}
    return data


def success(data=None, msg: str = "ok"):
    return {"code": 1, "msg": msg, "data": _serialize(data)}


def fail(msg: str = "error", code: int = 0, status_code: int = status.HTTP_400_BAD_REQUEST):
    return JSONResponse(status_code=status_code, content={"code": code, "msg": msg, "data": None})
