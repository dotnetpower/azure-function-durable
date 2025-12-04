from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class TodoItem:
    """
    SQL Trigger에서 사용되는 Todo Item 모델
    """
    Id: UUID
    order: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    completed: Optional[bool] = None
