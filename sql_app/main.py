'''
 * @author Nathan 
 * 
 * * 
 * 
 * (c) Copyright by  Limited.
 * 
 '''



 

import requests
from typing import List, Union
from fastapi.openapi.models import Server
from urllib import request, response
import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException,Body, status, Query
from fastapi.security import OAuth2PasswordBearer #security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models, schemas, crud # import the files
from database import engine, SessionLocal # import d functions
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse


from jwt_token import JWTBearer

#server2 = Server(url="http://127.0.0.1:8000")
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(bind=engine)


###proxy settings

 
 

##
#  Dependency


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# register API
@app.post("/register", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

# login API

        

@app.post("/login")
async def log_in(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    print("username: ", form_data.username, "password: ", form_data.password)
    db_user = crud.get_Login(db, username=form_data.username, password=form_data.password)
    if db_user == False :
        return {"message":"User not found"}
        raise HTTPException(status_code=400, detail="Wrong username/password")
    else:
        #get_token_url= f"http://127.0.0.1:8000/token/{form_data.username}"
       # print("url", get_token_url)
       # test_get_response = requests.get(get_token_url, headers = {'accept':'application/json'})
        #inp_post_response = request.post(get_token_url , json=form_data.username)
       # print(test_get_response)
        return {'message': 'logged in ', 'token': crud.create_access_token(form_data.username)}


# @app.post("/token/")
# async def read_items(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db) ):
#     print("username: ", form_data.username, "password: ", form_data.password)
#     db_user = crud.get_Login(db, username=form_data.username, password=form_data.password)
#     if db_user == False :
#         return {"message":"User not found"}
#         raise HTTPException(status_code=400, detail="Wrong username/password")
#     return {
#         "token": crud.create_access_token(form_data.username)
#     }

@app.get("/token/{username}")
async def read_items(username,db:Session = Depends(get_db)):
    return {
         "token": crud.create_access_token(username)
    }
 
# get user by username API
@app.get("/get_user/{username}", response_model=schemas.UserInfo,  dependencies=[Depends(JWTBearer())])
def get_user(username, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_user = crud.get_user_by_username(db, username=username)
    return db_user


#vulnerabl endpoint method permission
@app.post("/get_user/{username}",status_code=201 )
def get_user():
    print("hit the vulenrable endpoitn")
    #db_user = crud.get_user_by_username(db, username=user.username)
    return  {"added"}

# add items to DB API
@app.post("/add_item", response_model=schemas.ItemInfo)
def add_item(item: schemas.ItemInfo, db: Session = Depends(get_db)):
    db_item = crud.add_table(db=db, item=item)
    if db_item:
        raise HTTPException(status_code=200, detail="item registered")
    return f"Item Succesfully added"

# get item by id API
@app.get("/get_item/{id}", response_model=schemas.ItemAInfo, dependencies=[Depends(JWTBearer())], status_code=200)
def get_user(id, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_item = crud.get_item_by_id(db, id=id)
    if db_item is None:
        raise HTTPException(status_code=400, detail="No item found")
    return db_item

#vulerable endpoint to pollution
@app.get("/get_item/", response_model=schemas.ItemAInfo, status_code = 200)
def get_user(id: Union[List[str],None] = Query(default=None),db:Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id=id)
   # db_user = crud.get_user_by_username(db, username=username)
    if db_item is None :
        raise HTTPException(status_code=200, detail="item or User not  found")
    return {db_item}


# delete item by id API
@app.delete("/del_item/{id}", response_model=schemas.ItemAInfo, dependencies=[Depends(JWTBearer())])
def del_user(id, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_item = crud.delete_item_by_id(db, id=id)
    if db_item:
        raise HTTPException(status_code=200, detail="Item found to delete")
    else:
        raise HTTPException(status_code=400, detail="Item Not found to delete")
    return f"Item deleted successfully"

# add to cart by username and the items to be added API
@app.post("/add_to_cart/{username}", response_model=schemas.CartOwnerInfo, dependencies=[Depends(JWTBearer())])
def add_item(username, items:schemas.CartInfo, db: Session = Depends(get_db)):
    db_cart = crud.add_to_cart(db=db, username=username,items=items)
    if db_cart:
        raise HTTPException(status_code=200, detail="item registered to cart")
    return 

# delete items in the cart by id API
@app.delete("/del_cart_item/{id}", response_model=schemas.CartItemAInfo, dependencies=[Depends(JWTBearer())])
def del_user(id, db:Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_item = crud.delete_cart_item_by_id(db, id=id)
    if db_item:
        raise HTTPException(status_code=200, detail="Item found to delete")
    else:
        raise HTTPException(status_code=400, detail="Item Not found to delete")
    return

# mpesa payment API
@app.post("/payment")
def add_item(userphone:schemas.UserPayment, db: Session = Depends(get_db)):
    user_payment = crud.payment(db=db, phone_number=userphone.phonenumber,total=userphone.total)
    if user_payment:
        raise HTTPException(status_code=200, detail="payment Started")
    return 

# mpesa Callback API
@app.post("/callback")
def mpesa_callback(db: Session = Depends(get_db)):
    return {'success':"Payment was made successfully!"}


###/cart/username/itemId?updatePrice=2
@app.get("/cart/{username}/{itemId}/update",dependencies=[Depends(JWTBearer())])
def apiendpoint(db: Session = Depends(get_db),username: str="user_test",itemId: int=1, price: int=0):
    db_name  = crud.get_user_by_username(db, username=username)
    if db_name:
        existing_item = crud.get_item_by_id(db,id=itemId)
        if existing_item :
            action = crud.modify_price(db,existing_item,price)
            if action:
                return {'Success':"modified"}
        else:
            print("item not existing")
            return {'error': 'item not existing'}



@app.get("/redirect/")
async def redirect(url: str):
    #  regex = ("((http|https)://)(www.)?" +
    #          "[a-zA-Z0-9@:%._\\+~#?&//=]" +
    #          "{2,256}\\.[a-z]" +
    #          "{2,6}\\b([-a-zA-Z0-9@:%" +
    #          "._\\+~#?&//=]*)")
    #  p = re.compile(regex)
     if (url != None):
        # if(re.search(p, str)):
        response = RedirectResponse(url,status_code=303)
        return response
     else:
        return False
    
     return False
     
     
@app.get("/del_items")
def add_item( db: Session = Depends(get_db)):
    db_item = crud.delete_table_item(db)
    return 
 

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes, 
         servers=[{"url":"http://127.0.0.1:8000"}]

        
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)