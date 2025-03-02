from typing import TypeVar, Type, Any, Optional
from django.db.models import Field
from enum import Enum

E = TypeVar("E", bound=Enum)

class TextChoicesField(Field[E, E]):
    def __init__(
        self,
        choices_enum: Type[E],
        default: Optional[E] = None,
        **kwargs: Any,
    ) -> None: ...
