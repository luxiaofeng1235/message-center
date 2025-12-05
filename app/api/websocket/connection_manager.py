"""WebSocket 连接管理
更新日期: 2025-12-05
"""

from collections import defaultdict
from typing import DefaultDict

from fastapi import WebSocket


class ConnectionManager:
    """管理 user_id 到 websocket 的映射，并支持消息发送。"""

    def __init__(self) -> None:
        self.active_connections: DefaultDict[int, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket) -> None:
        if websocket in self.active_connections[user_id]:
            self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            self.active_connections.pop(user_id, None)

    async def send_personal_message(self, user_id: int, message: str) -> None:
        for connection in self.active_connections.get(user_id, []):
            await connection.send_text(message)

    def is_online(self, user_id: int) -> bool:
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0


manager = ConnectionManager()
