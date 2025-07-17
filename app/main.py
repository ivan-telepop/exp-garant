from http.client import HTTPException
from fastapi import FastAPI, Depends, Query
from fastapi_pagination import add_pagination, Page
from typing import List, Optional
from .schemas.schemas import PostReadSchema, PostStatisticSchema
from .dbapi.dependecies import get_async_session, Base, engine
from .dbapi.crud import get_posts, process_post_content, get_all_post
from sqlalchemy.ext.asyncio import AsyncSession

# Метаданные приложения
description = 'Ivan Goncharov - FastAPI Micro Service App'
title = "RestAPI приложение - pagination endpoints"

app = FastAPI(title=title, description=description)
add_pagination(app)

@app.get("/posts/", response_model=Page[PostReadSchema])
async def list_posts(
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
):
    """Асинхронный метод для получения постов: \n
    * В query параметрах можем передать - \n
    category: str \n
    keyword: str  \n
    page: int  \n
    size: int \n
    """
    return await get_posts(session, category, keyword)

@app.get("/posts/statistic/", response_model=List[PostStatisticSchema])
async def get_post_stats(
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
):
    """Асинхронный метод для получения статистики по постам:\n
    category: str \n
    keyword: str  \n
    """
    return await process_post_content(session, category, keyword)


@app.get('/all/{items}',response_model=List[PostReadSchema])
async def get_all_posts(items:int,session: AsyncSession = Depends(get_async_session)):
    """Асинхронный метод извлечения всех записей из базы данных \n 
    Параметр items:int  - колличество записей (обернул в abs чтобы не было отрицательных значений)"""
    return await get_all_post(session,items=int(abs(items))) # упрощенное решение



@app.on_event("startup")
async def startup():
    """Асинхронный метод для создания всех таблиц в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)