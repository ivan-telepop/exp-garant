from sqlalchemy.future import select
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Post
from schemas.schemas import PostStatisticSchema
from typing import List, Optional
from fastapi_pagination.ext.sqlalchemy import paginate
from utils.utils import get_analyzed_content



async def get_posts(session: AsyncSession, category: Optional[str] = None, keyword: Optional[str] = None):
    """Асинхронная функция для получения постов"""
    stmt = select(Post)
    if category:
        stmt = stmt.where(Post.category == category)
    if keyword:
        stmt = stmt.where(Post.content.ilike(f"%{keyword}%"))

    return await paginate(session, stmt)




async def get_all_post(session: AsyncSession, items: int):
    """Метод извлечения всех записей из БД \n 
    items:int колличество записей."""
    result = await session.stream(select(Post).limit(items))
    posts = []
    async for one in result.scalars():
        posts.append(one)
    return posts
 
 



async def process_post_content(session: AsyncSession, category: Optional[str] = None, keyword: Optional[str] = None) -> List[PostStatisticSchema]:
    """Асинхронная функция для анализа содержимого постов"""
    stmt = select(Post)
    if category:
        stmt = stmt.where(Post.category == category)
    if keyword:
        stmt = stmt.where(Post.content.ilike(f"%{keyword}%"))
    result = await session.stream(stmt)
    stats = []
    async for row in result:
        word_count = len(row[0].content.split()) # колличество слов в строке
        counted = get_analyzed_content(row[0].content) #Количество повторений
        stats.append(PostStatisticSchema(post_id=row[0].id, word_count=word_count,counted=counted))
    return stats
