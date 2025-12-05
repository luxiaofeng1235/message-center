"""实例心跳/注册服务
更新日期: 2025-12-05
"""

from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.instance import Instance
from app.schemas.instance import InstanceHeartbeat


class InstanceService:
    """实例心跳/注册服务。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def heartbeat(self, payload: InstanceHeartbeat) -> Instance:
        existing = await self.db.execute(select(Instance).where(Instance.instance_key == payload.instance_key))
        instance = existing.scalar_one_or_none()
        now = datetime.utcnow()
        if instance:
            await self.db.execute(
                update(Instance)
                .where(Instance.instance_key == payload.instance_key)
                .values(
                    host=payload.host,
                    pid=payload.pid,
                    last_heartbeat=now,
                    is_active=True,
                )
            )
            await self.db.commit()
            await self.db.refresh(instance)
            return instance
        instance = Instance(
            instance_key=payload.instance_key,
            host=payload.host,
            pid=payload.pid,
            started_at=now,
            last_heartbeat=now,
            is_active=True,
        )
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
