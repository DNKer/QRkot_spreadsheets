"""
Настройки Google API.
"""
from typing import Any, Generator

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

# Список разрешений
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Учётные данные сервисного аккаунта
INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}
# Объект учётных данных
cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service() -> Generator[Aiogoogle, Any, None]:
    """Основная точка входа для использования
    асинхронной библиотеки Google API."""
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
