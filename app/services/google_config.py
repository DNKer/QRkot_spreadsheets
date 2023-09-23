from typing import List


# Переменные для Google Sheets
G_DATE_FORMAT: str = '%Y/%m/%d %H:%M:%S'
G_VERSION_SHEETS: str = 'v4'
G_VERSION_DRIVE: str = 'v3'
G_LOCALE: str = 'ru_RU'
G_SHEET_TYPE: str = 'GRID'
G_SHEET_ID: int = 0
G_TITLE: str = 'Скорость закрытия проектов.'
G_ROW_COUNT: int = 100
G_COLUMN_COUNT: int = 11

HEADER: List[List[str]] = [
    ['Отчёт от', ''],
    ['Проекты по скорости закрытия'],
    ['Название проекта', 'Время сбора средств', 'Описание']
]

TITLE: str = 'Отчёт приложения QRKot на {}'
SPREADSHEET_BODY: dict = dict(
    properties=dict(
        locale=G_LOCALE,
    ),
    sheets=[dict(properties=dict(
        sheetType=G_SHEET_TYPE,
        sheetId=G_SHEET_ID,
        title=G_TITLE,
        gridProperties=dict(
            rowCount=G_ROW_COUNT,
            columnCount=G_COLUMN_COUNT,
        )
    ))]
)

SPREADSHEET_SIZE_ERR_MSG: str = (
    'Количество передаваемых данных не помещается в таблице!'
)