from datetime import datetime
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.crud.base import CRUDBase


ModelType = TypeVar('ModelType', bound=Base)
CRUDType = TypeVar('CRUDType', bound=CRUDBase)


def close_investment(obj: ModelType) -> None:
    """Устанавливает атрибут "Закрыто" с фиксацией времени."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def investment(invest_from: ModelType, invest_in: CRUDType, session: AsyncSession) -> ModelType:
    """Инвестирование пожертвований в незакрытые проекты."""
    objects = await invest_in.get_multi(session)
    for obj in objects:
        for_invest = invest_from.full_amount - invest_from.invested_amount
        investitions = obj.full_amount - obj.invested_amount
        to_invest = min(for_invest, investitions)
        obj.invested_amount += to_invest
        invest_from.invested_amount += to_invest
        if obj.full_amount == obj.invested_amount:
            close_investment(obj)
        if invest_from.full_amount == invest_from.invested_amount:
            close_investment(invest_from)
        break
    session.add_all((*objects, invest_from))
    await session.commit()
    await session.refresh(invest_from)
    return invest_from
