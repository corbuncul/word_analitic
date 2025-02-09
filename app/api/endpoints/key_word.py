from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_key_word_duplicate,
    check_key_word_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import key_word_crud
from app.schemas.key_word import (
    KeyWordCreate,
    KeyWordDB,
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[KeyWordDB],
)
async def get_all_flight(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех ключевых слов."""
    return await key_word_crud.get_all(session)


@router.post(
    '/',
    response_model=KeyWordDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_key_word(
    key_word: KeyWordCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание ключевого слова. Только для суперюзеров."""
    await check_key_word_duplicate(session, key_word.word)
    return await key_word_crud.create(key_word, session)


@router.delete(
    '/{key_word_id}',
    response_model=KeyWordDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_key_word(
    key_word_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление ключевого слова. Только для суперюзеров."""
    key_word = await check_key_word_exists(session, key_word_id)
    return await key_word_crud.remove(key_word, session)

