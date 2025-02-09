from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import KeyWord
from app.crud import CRUDBase
from app.schemas.key_word import KeyWordDB


key_word_crud = CRUDBase(KeyWord)
