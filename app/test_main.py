import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from .main import app
from fastapi import status
from fastapi.testclient import TestClient



client = TestClient(main.app)




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
    """ Test with statistic"""
    response = client.get("/posts/statistic/?category=Category_1&keyword=faoolas")
    assert response.status_code == 200
    




