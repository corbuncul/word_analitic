from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import key_word_crud, stop_word_crud
from app.services.morth import (
    delete_stopwords,
    normalise_text,
    tokenize_text
)
from app.schemas.analise import Words


router = APIRouter()


@router.post(
    '/',
    response_model=Words
)
async def create_new_key_word(
    text: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Анализ текста."""
    key_words = []
    stop_words = []
    tokens = normalise_text(delete_stopwords(tokenize_text(text)))
    for word in tokens:
        if await key_word_crud.get_id_by_word(word, session):
            key_words.append(word)
        elif await stop_word_crud.get_id_by_word(word, session):
            stop_words.append(word)
    data = {'key_words': key_words, 'stop_words': stop_words}
    return data
