import logging
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.exceptions import LogFileOutputError
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> None:
    """Обеспечивает доступ к БД используется в качестве
    зависимости (dependency) для объекта класса UserManager."""
    yield SQLAlchemyUserDatabase(session, User)


"""Определяем транспорт: токкен предаем
через заголовок HTTP-запроса Authorization: Bearer.
tokenUrl - эндпоинт для получения токена."""
bearer_transport = BearerTransport(tokenUrl=settings.TOKKEN_URL)


def get_jwt_strategy() -> JWTStrategy:
    """ Определяет стратегию: хранение токена в виде JWT.
    Параметры:
    secret - секретное слово, используемое для генерации токена
    lifetime_seconds - срок действия токена в секундах."""
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=settings.TOKKEN_LIFETIME_SEC
    )


auth_backend = AuthenticationBackend(
    name=settings.BACKEND_NAME_UNIC,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Описывает условия проверки (валидации) пароля пользователя.
    """

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Проверяет длину пароля и отсутствие email в пароле.
        Возвращаемое значение на англ. языке - требование тестов Y'prakticum."""
        if len(password) < settings.MAX_LENGHT_PASSWORD:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """Определяет действия после успешной регистрации пользователя."""
        try:
            logging.info(f'Пользователь {user.email} зарегистрирован.')
        except Exception as error:
            logging.exception(f'В процессе загрузки возникла ошибка: {error}')
            raise LogFileOutputError


async def get_user_manager(user_db=Depends(get_user_db)) -> None:
    """Возвращает объект класса UserManager."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
