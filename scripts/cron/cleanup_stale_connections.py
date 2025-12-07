"""
cleanup_stale_connections.py

主要功能：定时标记长时间未活跃的 WebSocket 连接为下线状态，避免“假在线”。
调度方式：可由 cron/systemd 定期执行（如每 1~5 分钟）。
------------------------------------------------------
作者: 团队/姓名
日期: 2025-12-06
版本: 1.0.0
"""

import asyncio
import os
from datetime import datetime, timedelta

from sqlalchemy import update

from app.db.session import async_session
from app.models.client_connection import ClientConnection

# 默认最大空闲 120 秒，可通过环境变量覆盖
MAX_IDLE_SECONDS = int(os.getenv("CONNECTION_MAX_IDLE_SECONDS", "120"))


async def cleanup() -> None:
    cutoff = datetime.utcnow() - timedelta(seconds=MAX_IDLE_SECONDS)
    now_ts = datetime.utcnow()
    async with async_session() as db:
        result = await db.execute(
            update(ClientConnection)
            .where(
                ClientConnection.disconnected_at.is_(None),
                ClientConnection.last_active_at < cutoff,
            )
            .values(disconnected_at=now_ts)
        )
        await db.commit()
        print(f"[cleanup] marked {result.rowcount} stale connections as disconnected (idle>{MAX_IDLE_SECONDS}s)")


def main() -> None:
    asyncio.run(cleanup())


if __name__ == "__main__":
    main()
