from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic.generics import GenericModel

T = TypeVar("T")


class PageMeta(BaseModel):
    total: int
    page: int
    page_size: int


class Page(GenericModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    meta: PageMeta
    items: Sequence[T]
