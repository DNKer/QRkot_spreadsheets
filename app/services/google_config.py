from typing import List


# Переменные для Google Sheets
DATE_FORMAT: str = '%Y/%m/%d %H:%M:%S'
VERSION_SHEETS: str = 'v4'
VERSION_DRIVE: str = 'v3'
ROW_COUNT: int = 100
COLUMN_COUNT: int = 11

HEADER: List[List[str]] = [
    ['Отчёт от', ''],
    ['Проекты по скорости закрытия'],
    ['Название проекта', 'Время сбора средств', 'Описание']
]

TITLE: str = 'Отчёт приложения QRKot на {}'
SPREADSHEET_BODY: dict = dict(
    properties=dict(
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Скорость закрытия проектов.',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))]
)

SPREADSHEET_SIZE_ERROR_MESSAGE: str = (
    'Невозможно создать таблицу размера {send_row} x {send_column}. '
    'Google-таблицы могут содержать не больше 5000000 ячеек и '
    'не более 18278 столбцов суммарно.'
)