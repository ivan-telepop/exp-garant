from collections import Counter

def get_analyzed_content(content: str) -> dict: 
    """Функция для анализа содержимого поля content - возвращает количество слов"""
    words = content.lower().split()
    word_freq = dict(Counter(words)) # to dict >> to schema 
    return word_freq
