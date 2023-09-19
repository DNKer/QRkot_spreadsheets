from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_closed,
    check_full_amount,
    check_name_duplicate,
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
    """Создать проект. Только для суперпользователей."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await investment(new_project, donation_crud, session)
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
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Изменить проект. Только для суперпользователя."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_closed(charity_project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        check_full_amount(charity_project, obj_in.full_amount)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


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
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    charity_project = check_project_is_invested(charity_project)
    return await charity_project_crud.remove(charity_project, session)
