from enum import Enum
from typing import Any, Optional, Type, TypeVar

from django.db.models import Field

E = TypeVar("E", bound=Enum)

class TextChoicesField(Field[E, E]):
    def __init__(
        self,
        choices_enum: Type[E],
        default: Optional[E] = None,
        **kwargs: Any,
    ) -> None: ...
