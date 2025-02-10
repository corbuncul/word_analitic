import re
import string

from spacy import load

ru_model = load('ru_core_news_sm')
en_model = load('en_core_web_sm')
stop_words = ru_model.Defaults.stop_words.union(en_model.Defaults.stop_words)


def has_cyrillic(text: str) -> bool:
    """Определяет на кириллице или латинице написан текст."""
    return bool(re.search('[а-яА-Я]', text))


def tokenize_text(text: str) -> list[str]:
    """Удаляет из текста знаки препинания и разбивает на слова."""
    clean = ''.join(
        [char.lower() for char in text if char not in string.punctuation]
    )
    return re.findall(r'\b\w+\b', clean)


def delete_stopwords(text: list[str]) -> list[str]:
    """Удаляет стоп-слова из списка."""
    return [word for word in text if word not in stop_words]


def normal_form(word: str) -> str:
    """Переводит слово в нормальную форму."""
    if has_cyrillic(word):
        lemma = ru_model(word)[0].lemma_
    else:
        lemma = en_model(word)[0].lemma_
    return lemma


def normalise_text(text: list[str]) -> list[str]:
    """Приводит слова в списке к нормальной форме."""
    return [normal_form(word) for word in text]
