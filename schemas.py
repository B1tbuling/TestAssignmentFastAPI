from pydantic import BaseModel, validator, StrictInt, StrictFloat

from exceptions import ValidationException
from services.date_formatter import convert_string_to_date


class ContributionInfo(BaseModel):
    date: str
    periods: StrictInt
    amount: StrictInt
    rate: StrictFloat | StrictInt

    @validator('date')
    def validate_date(cls, v):
        try:
            convert_string_to_date(v)
            return v
        except ValueError:
            raise ValidationException(error='Date is not valid')

    @validator('periods')
    def validate_periods(cls, v):
        if 1 <= v <= 60:
            return v
        raise ValidationException(error='Periods is not valid')

    @validator('amount')
    def validate_amount(cls, v):
        if 10000 <= v <= 3000000:
            return v
        raise ValidationException(error='Amount is not valid')

    @validator('rate')
    def validate_rate(cls, v):
        if 1 <= v <= 8:
            return v
        raise ValidationException(error='Rate is not valid')
