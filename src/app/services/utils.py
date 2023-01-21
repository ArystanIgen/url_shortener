from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from app.exceptions import InvalidIntervalError
from app.schemas.enums import DateCategoryEnum


def set_end_date(date_quantity: int, date_category: str) -> datetime:
    current_date = datetime.utcnow()
    if date_category == DateCategoryEnum.MONTH:
        return current_date + relativedelta(months=date_quantity)
    elif date_category == DateCategoryEnum.WEEK:
        return current_date + relativedelta(weeks=date_quantity)
    elif date_category == DateCategoryEnum.YEAR:
        if date_quantity != 1:
            raise InvalidIntervalError
        return current_date + relativedelta(years=1)
    return current_date + timedelta(days=date_quantity)
