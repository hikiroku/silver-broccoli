from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

class ValidityMixin(BaseModel):
    valid_from: datetime
    valid_until: Optional[datetime] = None
