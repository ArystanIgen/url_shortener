from datetime import datetime
from typing import Any, Dict
from pydantic import Field, BaseModel, HttpUrl, root_validator, PositiveInt
from pydantic.utils import GetterDict
from app.core.config import CONFIG

from app.schemas.enums import DateCategoryEnum


class LinkIn(BaseModel):
    original_link: HttpUrl = Field(title="Оригинальная ссылка")
    date_category: DateCategoryEnum = Field(default=DateCategoryEnum.DAY,
                                            title="Категория для формирования  срока действия сокращенной ссылки")
    date_quantity: PositiveInt = Field(default=90,
                                       title="Количество для формирования  срока действия сокращенной ссылки")


class LinkOut(BaseModel):
    shortened_link: str = Field(title="Сокращенная ссылка")
    original_link: HttpUrl = Field(title="Оригинальная ссылка")
    end_date: datetime = Field(title="Дата и время окончания срока действия сокращенной ссылки")

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def set_generated_link(cls, obj: GetterDict) -> Dict[str, Any]:
        url_dict = dict(obj.items())
        url_dict['shortened_link'] = f"{CONFIG.api.host}/{obj._obj.uuid}"

        return url_dict
