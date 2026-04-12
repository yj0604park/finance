from enum import Enum
from typing import Any, TypeVar

from django.db.models import Field

E = TypeVar("E", bound=Enum)

class TextChoicesField(Field[E, E]):
    def __init__(
        self,
        choices_enum: type[E],
        default: E | None = None,
        **kwargs: Any,
    ) -> None: ...
