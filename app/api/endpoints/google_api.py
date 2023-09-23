from typing import Dict, List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service, SCOPES
from app.core.user import current_superuser
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)

from app.crud.chartity_project import charity_project_crud


router = APIRouter()


@router.get(
    '/',
    dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
) -> List[Dict[str, str]]:
    """Создание отчета Google Sheets. Только для суперпользователей."""
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id, projects, wrapper_services
        )
    except Exception as error:
        raise Exception(
            f'В процессе создания отчета возникла ошибка: {error}'
        )
    if spreadsheet_id:
        return f'{SCOPES[0]}/d/{spreadsheet_id}'
    return 'Нет завершенных проектов: отчет Google Sheets не создан.'
