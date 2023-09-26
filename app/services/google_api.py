import copy
from datetime import datetime
from typing import Any, Dict, List, Tuple

from aiogoogle import Aiogoogle
from pydantic import ValidationError

from app.core.config import settings
from app.services.google_config import (
    DATE_FORMAT,
    MAX_COLUMNS_SIZE,
    MAX_ROWS_MUX_COLUMNS_SIZE,
    VERSION_DRIVE,
    VERSION_SHEETS,
    HEADER,
    SPREADSHEET_BODY,
    SPREADSHEET_SIZE_ERROR_MESSAGE,
    TITLE
)


def get_sorted_projects(projects: List) -> List[Tuple]:
    """Сортирует список проектов."""
    return sorted(
        [
            (
                project.name,
                (project.close_date - project.create_date),
                project.description,
            )
            for project in projects
        ],
        key=lambda x: x[1]
    )


async def spreadsheets_create(wrapper_services: Aiogoogle,
                              spreadsheet_body: Dict = None,
                              ) -> Any:
    """Создает эелектронную таблицу на Google-drive."""

    spreadsheet_body = (
        copy.deepcopy(SPREADSHEET_BODY) if spreadsheet_body is None
        else spreadsheet_body
    )
    spreadsheet_body['properties']['title'] = TITLE.format(
        datetime.now().strftime(DATE_FORMAT))
    service = await wrapper_services.discover(
        'sheets', VERSION_SHEETS)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


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
    service = await wrapper_services.discover('drive', VERSION_DRIVE)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: List,
        wrapper_services: Aiogoogle
) -> None:
    """Записывает полученную из базы данных информацию в документ с таблицами."""
    service = await wrapper_services.discover('sheets', VERSION_SHEETS)
    header = copy.deepcopy(HEADER)
    header[0][1] = datetime.utcnow()
    table_values = [
        *header,
        *[list(map(str, field)) for field in get_sorted_projects(projects)],
    ]
    rows = len(table_values)
    columns = max(map(len, table_values))
    if rows * columns > MAX_ROWS_MUX_COLUMNS_SIZE or columns > MAX_COLUMNS_SIZE:
        raise ValidationError(
            SPREADSHEET_SIZE_ERROR_MESSAGE.format(
                rows=rows, columns=columns
            )
        )

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption='USER_ENTERED',
            json={
                'majorDimension': 'ROWS',
                'values': table_values
            }
        )
    )
