from datetime import datetime

from pydantic import BaseModel


class EntityInsertMeta(BaseModel):
    created_at: datetime
    updated_at: datetime | None
