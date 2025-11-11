from datetime import date

from pydantic import BaseModel


class DevotionalResponse(BaseModel):
    reference: str
    text: str
    reflection: str
    date: date
