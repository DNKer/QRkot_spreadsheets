from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings


NOW_DATE_TIME: str = datetime.now().strftime(settings.DATE_FORMAT)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создает эелектронную таблицу на Google-drive."""
    service = await wrapper_services.discover('sheets', settings.G_VERSION_SHEETS)
    spreadsheet_body = {
        'properties': {'title': f'Отчёт приложения QRKot на {NOW_DATE_TIME}',
                       'locale': settings.G_LOCALE},
        'sheets': [{'properties': {'sheetType': settings.G_SHEET_TYPE,
                                   'sheetId': settings.G_SHEET_ID,
                                   'title': settings.G_TITLE,
                                   'gridProperties': {'rowCount': settings.G_ROW_COUNT,
                                                      'columnCount': settings.G_COLUMN_COUNT
                                                      }}
                    }]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Предоставляет права доступа вашему личному аккаунту к созданному документу."""
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', settings.G_VERSION_DRIVE)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: List,
        wrapper_services: Aiogoogle
) -> None:
    """Записывает полученную из базы данных информацию в документ с таблицами."""
    service = await wrapper_services.discover('sheets', settings.G_VERSION_SHEETS)
    # Формируем тело таблицы
    table_values: List[List[str]] = [
        ['Отчёт от', NOW_DATE_TIME],
        ['Проекты по скорости закрытия'],
        ['Название проекта', 'Время сбора средств', 'Описание']
    ]
    for project in projects:
        new_row: List[str] = [
            str(project['name']),
            str(project['duration']),
            str(project['description'])
        ]
        table_values.append(new_row)
    update_body = {
        'majorDimension': settings.G_MAJOR_DIMENSION_FILL,
        'values': table_values
    }
    len_table_values: int = len(table_values)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{len_table_values}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
