'''
 * @
 * 
  
 * 
 '''
from sqlalchemy.ext.compiler import compiles
from collections import UserList
from http.client import HTTPException
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
import models, schemas
import bcrypt
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64
from pydantic import ValidationError

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "abcd"  # should be kept secret
JWT_REFRESH_SECRET_KEY = "ohhhtest"    # should be kept secret

def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    print("TOKEN:", encoded_jwt)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt



# Get user by username function
def get_user_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.username == username).first()

# User registration function
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.UserInfo(username=user.username, password=hashed_password, fullname=user.fullname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Login Function
def get_Login(db: Session, username: str, password:str):
    db_user = db.query(models.UserInfo).filter(models.UserInfo.username == username).first()
    print(db_user)
    passw = bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8')) 
    return passw

# Get item by id function
def get_item_by_id(db: Session, id: int):
    return db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()

#get item by name
def get_item_price_by_name(db: Session, name: str):
    return db.query(models.ItemInfo.itemprice).filter(models.ItemInfo.itemname == name).first()

# Add items to DB function
def add_table(db: Session, item: schemas.ItemInfo):
    db_item = models.ItemInfo(itemname=item.itemname,itemprice=item.itemprice)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Delete item from DB by id function
def delete_item_by_id(db: Session, id: int):
    delitem = db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()
    if delitem is None:
        return
    db.delete(delitem)
    db.commit()
    return delitem

def delete_table_item(db: Session):
    deltable = db.query(models.ItemInfo).all()
    deluser = db.query(models.UserInfo).all()
    if deltable is None:
        return 
    for o in deltable:
        db.delete(o)
    if deluser is None:
        return 
    for x in deluser:
        db.delete(x)
    db.commit()

# Add to cart function
def add_to_cart(db: Session, username: str, items:models.CartInfo):
    user = db.query(models.UserInfo).filter(models.UserInfo.username == username).first()
    db_cart = models.CartInfo(ownername=user.id,itemname=items.itemname,quantity=items.quantity)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

# Delete item in the cart by id
def delete_cart_item_by_id(db: Session, id: int):
    delitem = db.query(models.CartInfo).filter(models.CartInfo.id == id).first()
    if delitem is None:
        return
    db.delete(delitem)
    db.commit()
    return delitem

def get_cart_by_id(db: Session, id: int):
    cartItem = db.query(models.CartInfo).filter(models.CartInfo.id == id).first()
    return cartItem
# Modify itemint
def modify_price(db: Session, id: int ,price: int):
   print("sitbon",id)
   #  db_item = models.ItemInfo(itemname=item.itemname, itemprice=item.itemprice)
   db_item = db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()
   print("sitbon2",db_item)
   # if not db_item:
      #  raise HTTPException(status_code=404, detail="Hero not found")
   if db_item is None:
    print("NOT TOKKKK")
   else:
    setattr(db_item,"itemprice" , price)
    print("here!")
    db.add(db_item)
    db.commit()
    return db_item
    

# Mpesa processing function(Not Complete Yet)
@classmethod
def payment(db:Session, phone_number:int , id:int):
    total = 0 
    # consumer_key = 'consumer_key'
    # consumer_secret = 'consumer_secret'
    # api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
   
    user = db.query(models.UserInfo).filter(models.UserInfo.id == id).first()
    if user:
        cartItem = get_cart_by_id(db, id)
        if cartItem:
            q = db.query(models.CartInfo.quantity).filter(models.UserInfo.id==id).first()
            item_name = db.query(models.CartInfo.itemname).filter(models.UserInfo.id==id).first()

            print("THEEEEE ITEM NAME :  ", item_name[0])
            price = get_item_price_by_name(db, item_name[0])
            total = q[0]*int(price[0])
                
            return {"message":"Your purchase has been executed successfully", "totalprice":int(total)}
        else:
            return {"message":"cart is empty!"}
    else:
        return {"message":"no user"}



    # r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    # mpesa_access_token = json.loads(r.text)
    # validated_mpesa_access_token = mpesa_access_token['access_token']

    # lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    # Business_short_code = 'short_code' # replace with the business short code
    # passkey = "pass_key"
    # data_to_encode = Business_short_code + passkey + lipa_time
    # online_password = base64.b64encode(data_to_encode.encode())
    # decode_password = online_password.decode('utf-8')

    # access_token = validated_mpesa_access_token
    # api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    # headers = {"Authorization": "Bearer %s" % access_token}
    # request = {
    #     "BusinessShortCode": Business_short_code,
    #     "Password": decode_password,
    #     "Timestamp": lipa_time,
    #     "TransactionType": "CustomerPayBillOnline",
    #     "Amount": total,
    #     "PartyA": phone_number,
    #     "PartyB": Business_short_code,
    #     "PhoneNumber": phone_number,
    #     "CallBackURL": "https://127.0.0.1:8000/callback", # Mpesa Callback
    #     "AccountReference": "User Payment",
    #     "TransactionDesc": "Testing stk push"
    # }
    # response = requests.post(api_url, json=request, headers=headers)
    # return response.text