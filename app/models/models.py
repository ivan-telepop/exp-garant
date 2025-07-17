from sqlalchemy import Column, Integer, String, Text
# from app.dbapi.dependecies import Base
from ..dbapi.dependecies import Base

class Post(Base):
    """ОРМ модель post"""
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    content = Column(Text, index=True)



