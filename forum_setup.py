import os
import datetime
import sys
from sqlalchemy import Column, ForeignKey,  Integer, String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ ='user'
	username = Column(String(100),nullable=False,unique=True)
	email = Column(String(250), nullable=False,primary_key=True)


class Post(Base):
	__tablename__ ='post'
	
	id = Column(Integer,primary_key=True)
	title = Column(String(100), nullable=False)
	content = Column(String(1000), nullable=False)
	date = Column(DateTime,default=datetime.datetime.now() )
	user_id = Column(String,ForeignKey('user.email'))
        user_name = Column(String(100),ForeignKey('user.username'))
	user = relationship('User', foreign_keys=[user_id])
        post = relationship('User', foreign_keys=[user_name])
    
class Comment(Base):
    __tablename__='comment'
    
    id = Column(Integer,primary_key=True)
    date = Column(DateTime,default=datetime.datetime.now())
    post_id = Column(Integer,ForeignKey('post.id'))
    text = Column(String(150))
    user_name =Column(String(100))
    post = relationship(Post)
    

engine = create_engine('sqlite:///forum.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
q1 = session.query(Post).all() # for debugging
