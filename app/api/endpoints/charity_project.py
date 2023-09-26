from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_closed,
    check_full_amount_is_less_than_invested,
    check_charity_project_name_duplicate,
    check_project_is_invested,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.chartity_project import charity_project_crud
from app.crud.donation import donation_crud

from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investment import investment


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    description='Создание нового `проекта.`',
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создать проект. Только для суперпользователя."""

    await check_charity_project_name_duplicate(
        charity_project.name, session
    )
    new_project = await charity_project_crud.create(
        charity_project,
        session,
        commit_choke=False
    )
    investment(
        new_project,
        await donation_crud.get_not_invested(session)
    )
    session.add(new_project)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    description='Получить список всех `проектов.`'
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получить перечень проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    description='Изменить `проект`'
)
async def partially_update_charity_project(
        project_id: int,
        project_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Изменить проект. Только для суперпользователя."""
    project_by_id = await charity_project_crud.get(project_id, session)
    check_charity_project_exists(project_by_id)
    check_closed(project_by_id)
    check_full_amount_is_less_than_invested(
        project_in.full_amount, project_by_id.invested_amount
    )
    await check_charity_project_name_duplicate(project_in.name, session)
    return await charity_project_crud.update(
        project_by_id, project_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    description='Удалить `проект.`'
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удалить проект. Только для суперпользователя."""
    charity_project = await charity_project_crud.get(project_id, session)
    check_project_is_invested(charity_project)
    return await charity_project_crud.remove(charity_project, session)
