from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PageMeta(BaseModel):
    total: int
    page: int
    page_size: int


class Page(GenericModel, Generic[T]):
    meta: PageMeta
    items: Sequence[T]
