from typing import List, Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


ModelType = TypeVar('ModelType', bound=Base)


class CRUDBase:
    """
    Базовый класс с набором стандартных методов.
    """

    def __init__(self, model) -> None:
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ) -> Optional[ModelType]:
        """Получить объект по id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        """Получить все объекты заданного класса."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            flag: Optional[bool] = True,
    ) -> ModelType:
        """Создать новый объект без коммита."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if flag:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ) -> ModelType:
        """Частичное обновление объекта."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ) -> ModelType:
        """Удаление объекта."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_invested(
            self,
            session: AsyncSession
    ) -> List[ModelType]:
        """Получить незавершенные проекты."""
        objects = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0
            ).order_by(self.model.create_date)
        )
        return objects.scalars().all()
