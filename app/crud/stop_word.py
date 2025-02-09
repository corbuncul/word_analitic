from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import StopWord
from app.crud import CRUDBase
from app.schemas.key_word import StopWordDB


stop_word_crud = CRUDBase(StopWord)
