from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.chartity_project import charity_project_crud
from app.models import CharityProject
from app.services.investment import close_investment


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверяет уникальность имени (project_name) проекта."""
    project_id = await charity_project_crud.get_charity_project_id_by_name(
        project_name, session)
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


def check_project_is_invested(charity_project: CharityProject, new_amount=None) -> None:
    """Проверка наличия суммы на счете (внесённой суммы)."""
    invested = charity_project.invested_amount
    if new_amount:
        if invested > new_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='При редактировании проекта должно быть запрещено устанавливать '
                'требуемую сумму меньше внесённой.'
            )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_charity_project_exists(
        project_name_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка существования проекта в базе данных."""
    charity_project = await charity_project_crud.get(project_name_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Проект по ID {project_name_id} не найден!'
        )
    return charity_project


def check_closed(charity_project: CharityProject):
    """Проверка закрыт ли проект, редактирование запрещено."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_full_amount(
    charity_project: CharityProject, full_amount: int
) -> CharityProject:
    """Проверка вложенных средств в базе данных."""
    if full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    if full_amount == charity_project.invested_amount:
        close_investment(charity_project)
    return charity_project
