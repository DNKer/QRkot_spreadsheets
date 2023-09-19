from sqlalchemy import Column, Integer, ForeignKey, Text

from .base import AbstractModel


class Donation(AbstractModel):
    """Модель `Пожертвование`."""

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)

    def __repr__(self):
        return (
            f'№{self.id}. Пожертвовано: {self.invested_amount}/{self.full_amount}'
        )
