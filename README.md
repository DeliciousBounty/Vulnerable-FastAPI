<h1 align="center">FastApi E-commerce Applications Endpoints 👋</h1>


## Code Samples

> Just to show you how the flow works here is the working example of the <b>get_item/id</b> endpoint.

<b>main.py</b>
```
@app.get("/get_item/{id}", response_model=schemas.ItemAInfo)
def get_user(id, db:Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, id=id)
    if db_item is None:
        raise HTTPException(status_code=400, detail="No item found")
    return db_item
```

The above piece of code handles the endpoint and calls the function <b>get_item_by_id</b> in the crud.py file for further processing.

<b>crud.py</b>
```
def get_item_by_id(db: Session, id: int):
    return db.query(models.ItemInfo).filter(models.ItemInfo.id == id).first()
```
The above piece of code handles the <b>get_item_by_id call</b> and queries the <b>DB</b> for an item with the <b>id passed in the parameter</b>


## Install
This Application works with mysql database, you need to create a database, check the database.py file for more information.
To create a new database:
```
mysql 
CREATE DATABASE restapi;
```
Then 

```
git clone 
source fastapienv/bin/activate
pip3 install -r requirements.txt
cd sql_app
```

## Usage

```sh
uvicorn main:app --reload
```
##Vulnerabilies
To test for vulnerabilities use the openapi_version1.json and buid [Cherrybomb](https://github.com/blst-security/cherrybomb) from the branch dev_last_nathan


Give a ⭐️ if this project helped you!
