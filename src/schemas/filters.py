from datetime import date

from pydantic import BaseModel, Field


class DateFilter(BaseModel):
    start_date: date = Field(description='Example: 2025-01-05')
    end_date: date = Field(description='Example: 2025-01-10')