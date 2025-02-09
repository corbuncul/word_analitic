import re
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from spacy import load
from spacy.lang.ru import Russian
from spacy.lang.en import English


def has_cyrillic(text: str) -> bool:
    """Определяет на кириллице или латинице написан текст."""
    return bool(re.search('[а-яА-Я]', text))


def tokenize_text(text: str) -> list[str]:
    """удаляет из текста знаки препинания и разбивает на слова."""
    clean = ''.join([char for char in text if char not in string.punctuation])
    return word_tokenize(clean)


def delete_stopwords(text: list[str]) -> list[str]:
    """Удаляет стоп-слова из списка."""
    stop_ru = stopwords.words('russian')
    stop_en = stopwords.words('english')
    stop_words = stop_en + stop_ru
    return [word for word in text if word not in stop_words]


def normal_form(word: str) -> str:
    """Переводит слово в нормальную форму."""
    if has_cyrillic(word):
        nlp = Russian()
        load_model = load('ru_core_news_sm')
    else:
        nlp = English()
        load_model = load('en_core_web_sm')
    lemma = load_model(word)[0].lemma_
    print(lemma, '\n')
    return lemma


def normalise_text(text: list[str]) -> list[str]:
    """Приводит слова в списке к нормальной форме."""
    return [normal_form(word) for word in text]
