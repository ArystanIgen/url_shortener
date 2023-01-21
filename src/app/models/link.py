from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import BaseModel


class LinkModel(BaseModel):
    __tablename__ = 'link'

    uuid = Column(String, unique=True, default=lambda: f"{uuid4()}", comment="Идентификатор сокращенной ссылки")
    original_link = Column(String, nullable=False, comment="Оригинальная ссылка")
    end_date = Column(DateTime, nullable=False, comment="Дата и время окончания срока действия сокращенной ссылки")
    date_category = Column(String(64), nullable=False,
                           comment="Категория для формирования  срока действия сокращенной ссылки")
    date_quantity = Column(Integer, nullable=False,
                           comment="Количество для формирования  срока действия сокращенной ссылки")
