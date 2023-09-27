# Переменные для Google Sheets
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
VERSION_SHEETS = 'v4'
VERSION_DRIVE = 'v3'
ROW_COUNT = 100
COLUMN_COUNT = 11

HEADER = [
    ['Отчёт от', ''],
    ['Проекты по скорости закрытия'],
    ['Название проекта', 'Время сбора средств', 'Описание']
]

TITLE = 'Отчёт приложения QRKot на {}'
SPREADSHEET_BODY = dict(
    properties=dict(
        locale='ru_RU',
    ),
    sheets=dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Скорость закрытия проектов.',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))
)

SPREADSHEET_SIZE_ERROR_MESSAGE = (
    'Невозможно создать таблицу размера {rows} x {columns}. '
    f'Число строк должно быть меньше {ROW_COUNT}, число '
    f'Число колонок должно быть меньше {COLUMN_COUNT}.'
)