import copy
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, List

from aiogoogle import Aiogoogle
from fastapi import HTTPException

from app.core.config import settings
from app.core.google_client import SCOPES
from app.services import google_config as g_const


async def spreadsheets_create(wrapper_services: Aiogoogle,
                              now_date_time: datetime,
                              spreadsheet_body: Dict = g_const.SPREADSHEET_BODY,
                              ) -> Any:
    """Создает эелектронную таблицу на Google-drive."""

    spreadsheet_body = (
        copy.deepcopy(g_const.SPREADSHEET_BODY) if spreadsheet_body is None
        else spreadsheet_body
    )
    spreadsheet_body['properties']['title'] = g_const.TITLE.format(
        str(now_date_time.strftime(g_const.G_DATE_FORMAT)))
    service = await wrapper_services.discover(
        'sheets', g_const.G_VERSION_SHEETS)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return (f'{SCOPES[0]}/d/{response["spreadsheetId"]}')


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Предоставляет права доступа вашему личному аккаунту к созданному документу."""
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', g_const.G_VERSION_DRIVE)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: List,
        wrapper_services: Aiogoogle,
        now_date_time: datetime,
) -> None:
    """Записывает полученную из базы данных информацию в документ с таблицами."""
    service = await wrapper_services.discover('sheets', g_const.G_VERSION_SHEETS)
    project_list: list = []
    project_list = sorted((
        (
            project.name,
            project.close_date - project.create_date,
            project.description
        ) for project in projects
    ), key=lambda x: x[1])
    header = copy.deepcopy(g_const.HEADER)
    header[0][1] = str(now_date_time)
    table_values = [
        *header,
        *[list(map(str, field)) for field in project_list],
    ]
    send_row, send_column = len(table_values), max(len(table) for table in header)
    if send_row > g_const.G_ROW_COUNT or send_column > g_const.G_COLUMN_COUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=g_const.SPREADSHEET_SIZE_ERR_MSG)

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{g_const.G_ROW_COUNT}C{g_const.G_COLUMN_COUNT}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
