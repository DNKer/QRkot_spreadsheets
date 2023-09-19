import logging
import os
import sys
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr


load_dotenv()


class Settings(BaseSettings):
    """
    Настройки проекта.
    """

    app_title: str = 'QRKot'
    app_author: str = 'DNK'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    description: str = 'Приложение благотворительного фонда поддержки котиков.'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    # Переменные для авторизации
    TOKKEN_URL: str = 'auth/jwt/login'
    TOKKEN_LIFETIME_SEC: int = 3600
    BACKEND_NAME_UNIC: str = 'jwt'
    MAX_LENGHT_PASSWORD: int = 3

    # Переменные для Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    # Переменные для отчетов Google-sheets
    DATE_FORMAT: str = '%Y/%m/%d %H:%M:%S'
    G_VERSION_SHEETS: str = 'v4'
    G_VERSION_DRIVE: str = 'v3'
    G_LOCALE: str = 'ru_RU'
    G_SHEET_TYPE: str = 'GRID'
    G_SHEET_ID: int = 0
    G_TITLE: str = 'Скорость закрытия проектов.'
    G_ROW_COUNT: int = 100
    G_COLUMN_COUNT: int = 11
    G_MAJOR_DIMENSION_FILL: str = 'ROWS'

    # Настройки логгирования
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(
                os.path.abspath('cat_charity_fund.log'), mode='a', encoding='UTF-8'),
            logging.StreamHandler(stream=sys.stdout)],
        format='%(asctime)s, %(levelname)s, %(message)s,'
               '%(name)s, %(message)s,', datefmt='%d-%m-%Y %H-%M',
    )

    class Config:
        env_file = '.env'


settings = Settings()
