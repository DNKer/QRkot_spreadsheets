from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Cхема для получения пользователя.
    """
    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Cхема для создания пользователя.
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    Cхема для обновления пользователя.
    """
    pass
