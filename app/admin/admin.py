from sqladmin import ModelView

from app.models import Keyword, Stopword, User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_superuser]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    category = "accounts"


class KeywordAdmin(ModelView, model=Keyword):
    column_list = [Keyword.id, Keyword.word]
    name = "Ключевое слово"
    name_plural = "Ключевые слова"
    icon = 'fa-solid fa-file-text'
    category = "keywords"
    column_searchable_list = [Keyword.word]
    column_sortable_list = [Keyword.word]


class StopwordAdmin(ModelView, model=Stopword):
    column_list = [Stopword.id, Stopword.word]
    name = "Стоп-слово"
    name_plural = "Стоп-слова"
    icon = "fa-solid fa-file-text"
    category = "stopwords"
    column_searchable_list = [Stopword.word]
    column_sortable_list = [Stopword.word]
