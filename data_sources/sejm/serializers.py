from enum import StrEnum, auto

from pydantic import BaseModel, Field


class PublisherType(StrEnum):
    DU = auto()
    MP = auto()


class ActInfo(BaseModel):
    address: str
    publisher: str
    year: int
    pos: int
    title: str
    promulgation: str | None = None
    announcement_date: str | None = Field(alias="announcementDate", default=None)
    change_date: str = Field(alias="changeDate")
    eli: str = Field(alias="ELI")
    type: str
    status: str


class ActsInfo(BaseModel):
    items: list[ActInfo]
    offset: int
    count: int
    total_count: int = Field(alias="totalCount")
