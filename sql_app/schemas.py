'''
 * @author 
 * 
 * * Created:   16.07.2020
 * 
 * (c) Copyright by Devligence Limited.
 * 
 '''
 
from typing import List
from pydantic import BaseModel,Field
from sqlalchemy import Column, Integer, String
from database import Base
# base schema for user data
class UserInfoBase(BaseModel):
    username:str = Field(...,description= "username of the website", min_length=3,max_length=15, example= "user_test")
    fullname:str = Field(..., description= "username and last name", max_length=20, example= "John Doe")

#schema for user creation(registration)
class UserCreate(UserInfoBase):
    password:str = Field(...,description= "passwords of the website", max_length=15)

class UserInfo(UserInfoBase):
    id:int 

    class Config:
        orm_mode = True

#base schema for user login
class UserLogin(BaseModel):
    username:str =Field(...,description= "username of the website", min_length=3,max_length=15, example= "User1")
    password:str =Field(..., description= "passwords of the website", max_length=15)

#base schema for items
class ItemInfo(BaseModel):
    itemname:str = Field(..., description= "name of the item", min_length=3,max_length=20, example= "fruit") 
    itemprice:int =Field(..., description= "price of the iten", minimum=1, example= "1")

#inherits from item data schema used for getting item by id
class ItemAInfo(ItemInfo):
    id:int

    class Config:
        orm_mode = True

#base schema for relating a cart to it's user
class CartOwnerInfo(BaseModel):
    username:str =Field(...,description= "username cart owner", min_length=3,max_length=15, example= "user_test")

#base schema for adding items to cart
class CartInfo(BaseModel):
    itemname:str = Field(...,description= "item name", min_length=3,max_length=15, example= "Fruit")
    quantity:int =Field(...,description= "quantity", minimum=1, type= "integer",example= "1")

#base schema for getting items in the cart by id
class CartItemAInfo(CartInfo):
    id:int

    class Config:
        orm_mode = True

#base schema for the payment api
class UserPayment(BaseModel):
    phonenumber:int = Field( ...,description= "Phone number ", minimum=9,maximum=9, example= "+95343253453")
    id: int = Field( ...,description= "User Id  ", minimum=0,maximum=100, example= "1")


class ItemPriceInfo(BaseModel):
    itemname:str = Field(..., description= "name of the item", min_length=3,max_length=20, example= "fruit") 
    itemprice:int =Field(..., description= "price of the iten", minimum=1, example= "1")
