from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CrudCharityProject(CRUDBase):

    @staticmethod
    async def get_charity_project_id_by_name(
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        """Получить ID проекта по его имени."""
        db_charity_project_id = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_project_name
            )
        )
        return db_charity_project_id.scalars().first()

    @staticmethod
    async def get_projects_by_completion_rate(
            session: AsyncSession,
    ) -> List[Dict[str, str]]:
        """Получить НЕсортированный список со всеми закрытыми проектами."""
        close_projects = await session.execute(
            select([CharityProject],).where(
                CharityProject.fully_invested is True)
        )
        return close_projects.scalars().all()


charity_project_crud = CrudCharityProject(CharityProject)
