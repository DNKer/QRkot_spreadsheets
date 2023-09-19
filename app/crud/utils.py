from datetime import datetime
from enum import Enum
from typing import List


class SortingAttrClass(str, Enum):
    """Enum-класс параметра сортировки."""

    NAME: str = 'name'
    DURATION: datetime = 'duration'


def get_sorted_list_rate(projects: List, sorting_attribute: SortingAttrClass) -> List:
    """Функция сортировки списка projects.
    Attributes
    ----------
    projects : List
        список для сортировки
    sorting_attribute : Enam
        параметр сортировки."""
    project_list: List = []
    for project in projects:
        project_list.append({
            'name': project.name,
            'duration': project.close_date - project.create_date,
            'description': project.description
        })
    return sorted(project_list, key=lambda x: x[sorting_attribute])
