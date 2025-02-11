from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def check_word_duplicate(
    session: AsyncSession, word: str, crud_model, model_name: str
):
    """Общая проверка на дубликаты"""
    if await crud_model.get_id_by_word(word, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Такое {model_name} уже существует!'
        )


async def check_word_exists(
    session: AsyncSession,
    word: str,
    crud_model,
    model_name: str
):
    """Общая проверка существования слова (ключевого или стоп-слова)"""
    word_id = await crud_model.get_id_by_word(word, session)
    if word_id is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'{model_name} не найдено!'
        )
    return await crud_model.get(word_id, session)
