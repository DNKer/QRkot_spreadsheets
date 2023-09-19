"""
Импорт производим в пределах одного Python-пакета
app/models для простоты, чтобы не разбираться,
какие между моделями отношения.
"""

from .charity_project import CharityProject # noqa
from .donation import Donation # noqa
from .user import User # noqa
