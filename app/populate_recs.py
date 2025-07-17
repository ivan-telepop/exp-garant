import asyncio
import random
import string
from app.models.models import Post
from app.dbapi.dependecies import engine,async_session,Base

# Скрипт наполняющий базу данных записямис случайным набором слов.


# random data generation
def random_word(length=5):
    """ Функция генерирующая случайные данные - строки как слова """
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_sentence(min_words=5, max_words=20):
    """ Функция генерирующая случайные данные - мок строки похожие на предложения """
    words = [random_word(random.randint(3, 10)) for _ in range(random.randint(min_words, max_words))]
    return ' '.join(words).capitalize() + '.'


async def populate_posts():
    """ Функция создающая записи в базе данных """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    categories = [f"Category_{i}" for i in range(1, 26)]
    total_posts = random.randint(200, 250)

    posts = [
        Post(category=random.choice(categories),content=random_sentence())
        for _ in range(total_posts)
        ]

    async with async_session() as session:
        session.add_all(posts)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(populate_posts())
