from sqlalchemy import Column, String, Text

from app.models.base import AbstractModel


class CharityProject(AbstractModel):
    """Модель `Благотворительный проект`."""

    name = Column(String(100), nullable=False, unique=True, )
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{self.name}. Собрано: {self.invested_amount}/{self.full_amount}'
        )
