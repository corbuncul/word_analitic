from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_word_duplicate,
    check_word_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import stop_word_crud
from app.schemas.stop_word import StopwordCreate, StopwordDB
from app.services.morph import normal_form


router = APIRouter()


@router.get(
    '/',
    response_model=list[StopwordDB],
)
async def get_all_stop_words(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех стоп-слов."""
    return await stop_word_crud.get_all(session)


@router.post(
    '/',
    response_model=StopwordDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_stop_word(
    stop_word: StopwordCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание стоп-слова. Только для суперюзеров."""
    stop_word.word = normal_form(stop_word.word.lower())
    await check_word_duplicate(
        session, stop_word.word, stop_word_crud, 'стоп-слово'
    )
    return await stop_word_crud.create(stop_word, session)


@router.post(
        '/upload-file', response_model=list[StopwordDB],
        dependencies=[Depends(current_superuser)]
    )
async def upload_stop_words_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session)
):
    """Загрузка списка стоп-слов из файла."""
    lines = (await file.read()).decode("utf-8").splitlines()
    created_objs = []
    
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        lemma = normal_form(cleaned.lower())
        await check_word_duplicate(
            session, lemma, stop_word_crud, 'стоп-слово'
        )
        new_sw = await stop_word_crud.create(
            StopwordCreate(word=lemma), session
        )
        created_objs.append(new_sw)
    return created_objs


@router.delete(
    '/{stop_word_id}',
    response_model=StopwordDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_stop_word(
    stop_word_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление стоп-слова. Только для суперюзеров."""
    stop_word = await check_word_exists(
        session, stop_word_id, stop_word_crud, 'Стоп-слово'
    )
    return await stop_word_crud.remove(stop_word, session)
