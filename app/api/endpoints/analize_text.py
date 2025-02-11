from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import key_word_crud, stop_word_crud
from app.services.morph import (
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
async def analyze_text(
    text: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Анализ текста."""
    if not text.strip():
        raise HTTPException(
            status_code=400, detail='Текст для анализа не может быть пустым.'
        )
    tokens = normalise_text(delete_stopwords(tokenize_text(text)))
    if not tokens:
        return JSONResponse(content={'key_words': [], 'stop_words': []})
    key_words_set = set(await key_word_crud.get_all_words(session))
    stop_words_set = set(await stop_word_crud.get_all_words(session))
    key_words = [word for word in tokens if word in key_words_set]
    stop_words = [word for word in tokens if word in stop_words_set]
    return JSONResponse(
        content=jsonable_encoder(
            {'key_words': key_words, 'stop_words': stop_words}
        )
    )
