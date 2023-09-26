from typing import Dict, List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from googleapiclient.errors import HttpError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.chartity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value
)

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
    projects = await charity_project_crud.get_projects_fully_invested(
        session
    )
    try:
        spreadsheet_id = await spreadsheets_create(wrapper_services)
        await set_user_permissions(spreadsheet_id, wrapper_services)
        await spreadsheets_update_value(
            spreadsheet_id, projects, wrapper_services
        )
    except HttpError as error:
        raise HTTPException(error.status_code,
                            detail=error.detail)
    return spreadsheet_id['spreadsheetUrl']
