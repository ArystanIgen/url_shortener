from datetime import datetime
from pydantic import Field, BaseModel, HttpUrl, PositiveInt
from app.schemas.enums import DateCategoryEnum


class LinkCreate(BaseModel):
    original_link: HttpUrl = Field(title="Оригинальная ссылка")
    date_category: DateCategoryEnum = Field(default=DateCategoryEnum.DAY,
                                            title="Категория для формирования  срока действия сокращенной ссылки")
    date_quantity: PositiveInt = Field(default=90,
                                       title="Количество для формирования  срока действия сокращенной ссылки")
    end_date: datetime = Field(title="Дата и время окончания срока действия сокращенной ссылки")


class LinkUpdate(BaseModel):
    original_link: HttpUrl = Field(title="Оригинальная ссылка")
    date_category: DateCategoryEnum = Field(default=DateCategoryEnum.DAY,
                                            title="Категория для формирования  срока действия сокращенной ссылки")
    date_quantity: PositiveInt = Field(default=90,
                                       title="Количество для формирования  срока действия сокращенной ссылки")
    end_date: datetime = Field(title="Дата и время окончания срока действия сокращенной ссылки")
