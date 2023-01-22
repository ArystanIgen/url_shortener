from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from app.exceptions import InvalidExpirationDateError
from app.schemas.enums import DateCategoryEnum


def set_end_date(date_quantity: int, date_category: str) -> datetime:
    current_date = datetime.utcnow()
    if date_category == DateCategoryEnum.MONTH:
        new_date = current_date + relativedelta(months=date_quantity)
    elif date_category == DateCategoryEnum.WEEK:
        new_date = current_date + relativedelta(weeks=date_quantity)
    elif date_category == DateCategoryEnum.YEAR:
        new_date = current_date + relativedelta(years=date_quantity)
    else:
        new_date = current_date + timedelta(days=date_quantity)

    if (new_date - current_date) >= timedelta(days=366):
        raise InvalidExpirationDateError

    return new_date
