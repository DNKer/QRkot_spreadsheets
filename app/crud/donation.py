from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_user_donations(
        self, session: AsyncSession, user: User
    ) -> Optional[Donation]:
        """Получение всех пожертвований пользователя."""
        select_user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return select_user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
