
'''

 * 
 '''
from pydantic import BaseModel, Field
from fastapi.openapi.utils import get_openapi

from typing import Text
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import LONGTEXT, TEXT
from database import Base

# User Database Model
class UserInfo(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True, index=True)
    username =Column(String(24), unique=True)
    password = Column(LONGTEXT)
    fullname = Column(String(24), unique=True)
    
class ItemInfo(Base):
    __tablename__ = "item_info"
    id = Column(Integer, primary_key=True, index=True)
    itemname= Column(String(16), unique=True)
    itemprice = Column(Integer)

# User Cart Databse Model
class CartInfo(Base):
    __tablename__ = "cart_info"
    id = Column(Integer, primary_key=True, index=True)
    ownername= Column(String(24), unique=True)
    itemname= Column(String(16), unique=True)
    quantity = Column(Integer)
   # itemprice = Column(Integer)
   