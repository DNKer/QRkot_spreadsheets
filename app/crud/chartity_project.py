from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.utils import get_sorted_list_rate, SortingAttrClass
from app.models.charity_project import CharityProject


class CrudCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Получить ID проекта по его имени."""
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return db_charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[Dict[str, str]]:
        """Получить отсортированный список со всеми закрытыми проектами."""
        close_projects = await session.execute(
            select([CharityProject],).where(
                CharityProject.fully_invested is True)
        )
        close_projects = close_projects.scalars().all()
        sorting_attribute = SortingAttrClass.DURATION
        return get_sorted_list_rate(close_projects, sorting_attribute)


charity_project_crud = CrudCharityProject(CharityProject)
