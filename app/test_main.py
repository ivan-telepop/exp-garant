import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from main import app
from fastapi import status
from fastapi.testclient import TestClient
from fastapi_pagination import add_pagination


add_pagination(app)

client = TestClient(app)

def test_docs():
    """Тест swagger"""
    response = client.get("/docs")
    assert response.status_code == 200
    
def test_redoc():
    """Тест redoc"""
    response = client.get("/redoc")
    assert response.status_code == 200
    
    
def test_get_all():
    """Тест get all """
    response = client.get("/all/10")
    assert response.status_code == 200
    
def test_get_post_stats():
    """ Тест получения статистики постов"""
    response = client.get("/posts/?category=Category_14&keyword=xobiewy&page=1&size=50")
    assert response.status_code == 200
    
def test_get_posts_analysed():
    """Тест получения статистики постов"""
    response = client.get("/posts/statistic/?category=Category_14&keyword=xobiewy")
    assert response.status_code == 200
    
    
    
# Упрощенные тесты не для продакшен проектов.