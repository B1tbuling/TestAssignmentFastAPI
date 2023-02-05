from pydantic import BaseModel, Field, validator
from fastapi import HTTPException

from services.date_formatter import convert_string_to_date


class ContributionInfo(BaseModel):
    date: str
    periods: int # = Field(ge=1, le=60)
    amount: int # = Field(ge=10000, le=3000000)
    rate: float # = Field(ge=1, le=8)

    @validator('date')
    def validate_date(cls, v):
        try:
            convert_string_to_date(v)
            return v
        except ValueError:
            raise HTTPException(status_code=400, detail='Date is not valid')

    @validator('periods')
    def validate_periods(cls, v):
        if 1 <= v <= 60:
            return v
        raise HTTPException(status_code=400, detail='Periods is not valid')

    @validator('amount')
    def validate_amount(cls, v):
        if 10000 <= v <= 3000000:
            return v
        raise HTTPException(status_code=400, detail='Amount is not valid')

    @validator('rate')
    def validate_rate(cls, v):
        if 1 <= v <= 8:
            return v
        raise HTTPException(status_code=400, detail='Rate is not valid')
