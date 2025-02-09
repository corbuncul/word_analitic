from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.key_word import key_word_crud
from app.crud.stop_word import stop_word_crud
from app.models import KeyWord, StopWord


async def check_key_word_duplicate(
    session: AsyncSession,
    word: str,
) -> None:
    """Провверка на дублирование ключевого слова"""
    key_word_id = await key_word_crud.get_id_by_word(
        word, session
    )
    if key_word_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Такое ключевое слово уже существует!',
        )


async def check_key_word_exists(
    session: AsyncSession,
    word: str,
) -> KeyWord:
    """Проверка существования ключевого слова"""
    key_word_id = await key_word_crud.get_id_by_word(
        word, session
    )
    if key_word_id is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Ключевое слово не найдено!'
        )
    key_word = await key_word_crud.get(key_word_id, session)
    return key_word


async def check_stop_word_duplicate(
    session: AsyncSession,
    word: str,
) -> None:
    """Провверка на дублирование стоп-слова"""
    stop_word_id = await stop_word_crud.get_id_by_word(
        word, session
    )
    if stop_word_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Такое стоп-слово уже существует!',
        )


async def check_key_word_exists(
    session: AsyncSession,
    word: str,
) -> StopWord:
    """Проверка существования стоп-слова"""
    stop_word_id = await stop_word_crud.get_id_by_word(
        word, session
    )
    if stop_word_id is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Стоп-слово не найдено!'
        )
    stop_word = await stop_word_crud.get(stop_word_id, session)
    return stop_word
