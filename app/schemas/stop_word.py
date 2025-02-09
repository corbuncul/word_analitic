from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)
from app.core.db import MAX_LENGHT


class StopWordCreate(BaseModel):
    word: str = Field(..., min_length=1, max_length=MAX_LENGHT)
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class StopWordDB(StopWordCreate):
    id: int
