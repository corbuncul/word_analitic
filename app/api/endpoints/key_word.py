from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_word_duplicate,
    check_word_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import key_word_crud
from app.schemas.key_word import (
    KeyWordsCreateList,
    KeywordCreate,
    KeywordDB,
)
from app.services.morph import normal_form


router = APIRouter()


@router.get(
    '/',
    response_model=list[KeywordDB],
)
async def get_all_keywords(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех ключевых слов."""
    return await key_word_crud.get_all(session)


@router.post(
    '/',
    response_model=KeywordDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_key_word(
    key_word: KeywordCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание ключевого слова. Только для суперюзеров."""
    key_word.word = normal_form(key_word.word.lower())
    await check_word_duplicate(
        session, key_word.word, key_word_crud, 'ключевое слово'
    )
    return await key_word_crud.create(key_word, session)


@router.post(
        '/batch', response_model=list[KeywordDB],
        dependencies=[Depends(current_superuser)]
    )
async def create_key_words_batch(
    words_in: KeyWordsCreateList,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание нескольких ключевых слов за один раз."""
    created_objs = []
    for word in words_in.words:
        lemma = normal_form(word.lower())
        await check_word_duplicate(
            session, lemma, key_word_crud, 'ключевое слово'
        )
        new_kw = await key_word_crud.create(KeywordCreate(word=lemma), session)
        created_objs.append(new_kw)
    return created_objs


@router.delete(
    '/{key_word_id}',
    response_model=KeywordDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_key_word(
    key_word_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление ключевого слова. Только для суперюзеров."""
    key_word = await check_word_exists(
        session, key_word_id, key_word_crud, 'Ключевое слово'
    )
    return await key_word_crud.remove(key_word, session)


@router.post(
        '/upload-file', response_model=list[KeywordDB],
        dependencies=[Depends(current_superuser)]
    )
async def upload_key_words_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
):
    lines = (await file.read()).decode('utf-8').splitlines()
    created_objs = []
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        lemma = normal_form(cleaned.lower())
        await check_word_duplicate(
            session, lemma, key_word_crud, 'ключевое слово'
        )
        new_sw = await key_word_crud.create(KeywordCreate(word=lemma), session)
        created_objs.append(new_sw)
    return created_objs
