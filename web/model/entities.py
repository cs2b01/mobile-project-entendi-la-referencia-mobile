from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector
import datetime

class User(connector.Manager.Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email     = Column(String(200))
    name     = Column(String(150))
    lastname   = Column(String(150))
    password = Column(String(50))
    username    = Column(String(50))
    record     = Column(Integer)
    uploads     = Column(Integer)


class Category(connector.Manager.Base):
    __tablename__ = 'categories'
    id    = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name  = Column(String(50))

class Question(connector.Manager.Base):
    __tablename__ = 'questions'
    id            = Column(Integer, Sequence('question_id_seq'), primary_key=True)
    statment     = Column(String(1500))
    answer      = Column(String(1500))
    wrong1   = Column(String(1500))
    wrong2   = Column(String(1500))
    wrong3   = Column(String(1500))
    category_id  = Column(Integer, ForeignKey('categories.id'))
    category     = relationship(Category, foreign_keys=[category_id])
