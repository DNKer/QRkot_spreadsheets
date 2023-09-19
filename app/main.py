"""
QRKot Spreadsheets.
This is C@t charity project (https://github.com/DNKer/cat_charity_fund) upgrade
Copyright (C) 2023 Authors: Dmitry Korepanov, Yandex practikum
License Free
Version: 1.0.0.2023.
"""

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser


app = FastAPI(title=settings.app_title, description=settings.description)
app.include_router(main_router)


@app.on_event('startup')
async def startup():
    """Автоматическое создание суперпользователя."""
    await create_first_superuser()
