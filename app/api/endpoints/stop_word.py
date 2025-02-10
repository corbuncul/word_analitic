from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_stop_word_duplicate,
    check_stop_word_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import stop_word_crud
from app.schemas.stop_word import (
    StopWordCreate,
    StopWordDB,
)
from app.services.morth import normal_form


router = APIRouter()


@router.get(
    '/',
    response_model=list[StopWordDB],
)
async def get_all_flight(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех стоп-слов."""
    return await stop_word_crud.get_all(session)


@router.post(
    '/',
    response_model=StopWordDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_stop_word(
    stop_word: StopWordCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание стоп-слова. Только для суперюзеров."""
    stop_word.word = normal_form(stop_word.word.lower())
    await check_stop_word_duplicate(session, stop_word.word)
    return await stop_word_crud.create(stop_word, session)


@router.delete(
    '/{stop_word}',
    response_model=StopWordDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_stop_word(
    stop_word: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление стоп-слова. Только для суперюзеров."""
    stop_word_db = await check_stop_word_exists(session, stop_word)
    return await stop_word_crud.remove(stop_word_db, session)
