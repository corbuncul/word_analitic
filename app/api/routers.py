from fastapi import APIRouter

from app.api.endpoints import (
    key_word_router,
    stop_word_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(
    key_word_router,
    prefix='/key_word',
    tags=['Ключевые слова'],
)
main_router.include_router(
    stop_word_router,
    prefix='/stop_word',
    tags=['Стоп-слова']
)
main_router.include_router(user_router)
