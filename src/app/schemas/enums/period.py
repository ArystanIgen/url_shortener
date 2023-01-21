# App Imports
from app.schemas.enums.base import StrEnum


class DateCategoryEnum(StrEnum):
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    YEAR = 'YEAR'
