from datetime import datetime
from typing import List

from app.models.base import CharatyDonationModel


def investment(
    target: CharatyDonationModel,
    sources: List[CharatyDonationModel]
) -> List[CharatyDonationModel]:
    """Инвестирование пожертвований в незакрытые проекты."""
    result = []
    if not target.invested_amount:
        target.invested_amount = 0
    for source in sources:
        to_invest = target.full_amount - target.invested_amount
        for obj in (target, source):
            obj.invested_amount += to_invest
            if obj.full_amount == obj.invested_amount:
                obj.close_date = datetime.now()
                obj.fully_invested = True
        result.append(source)
        if target.fully_invested:
            break
    return result
