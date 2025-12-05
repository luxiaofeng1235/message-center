from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.admin_user import AdminUser


async def init_db(db: AsyncSession) -> None:
    # 简单示例：如需初始化超级管理员，可在此处创建
    exists = await db.scalar(
        AdminUser.__table__.select().limit(1)  # type: ignore[attr-defined]
    )
    if exists:
        return
    admin = AdminUser(username="admin", password_hash=get_password_hash("admin"))
    db.add(admin)
    await db.commit()
