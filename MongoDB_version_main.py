from settings import *

Base_dir = os.getcwd()
vip_token = 'efai'


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: list = []

class Message(BaseModel):
    message: str


# FastAPI Setting || dorc_url=None, redoc_url=None, openapi_url=None
app = FastAPI(title="EFAI API Testing")
security = HTTPBasic()
x_api_token = ''

def reset_token():
    global x_api_token
    x_api_token = ''


# local use
@app.get("/get_token/", tags=['Token'])
async def get_token(x_api_key: Optional[str]):
    global x_api_token
    if x_api_key == vip_token:
        x_api_token = identity_generator()
        print('x_api_token: ', x_api_token)
        t = Timer(14400.0, reset_token)
        t.start()
        return {"token": x_api_token}
    else:
        Message = {"Status": "Error", "Message": "x_api_key is error"}
        return JSONResponse(status_code=404, content=Message)


@app.get("/views_users/", tags=["database"])
async def get_users(token: Optional[str]):
    print('token: ', token)
    print("x_api_token: ", x_api_token)
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)

    # MongoDb
    mon_table = mongo_db('db_table')
    result = [n for n in mon_table.find({}, {"_id": 0, "id": 1, "Name": 1, "Age": 1, "Feature": 1, "Level": 1})]
    data = {"User_data": result}
    return data


@app.get("/views_country/", tags=['database'])
async def get_country(token: Optional[str]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)

    # MongoDb
    mon_table = mongo_db('country')
    result = [n for n in mon_table.find({}, {"_id": 0, "id": 1, "country": 1, "area": 1, "population": 1})]
    data = {"User_data": result}
    return data

@app.get("/views_test_result", tags=['database'])
async def get_test_result(token: Optional[str]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    mon_table = mongo_db('Test_result')
    result = {"Data": [n for n in mon_table.find({}, {"_id":0})]}
    return result

# db
# ---------------------------------- #
@app.post('/db/insert_user_data', tags=['database'])
async def insert_user_data(token: Optional[str], name: Optional[str], age: Optional[int],
                 feature: Optional[str], level: Optional[int]):
    check = []
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)

    # MongoDB
    result = [check.append(n['id']) for n in mon_table.find({}, {"_id": 0, "id": 1} )]
    if check:
        next_num = max(check) + 1
    else:
        next_num = 1
    mon_table = mongo_db("db_table")
    mon_table.insert_one( {"id": next_num, "Name": f'{name}',"Age": age, "Feature": f'{feature}', "Level": level} )
    return "OK"


@app.post('/db/insert_country_data', tags=['database'])
async def insert_country_data(token: Optional[str], country: Optional[str],
                 area: Optional[str], population: Optional[int]):
    check = []
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    
    # MongoDB
    # Search id
    mon_table = mongo_db("country")
    result = [check.append(n['id']) for n in mon_table.find({}, {"_id": 0, "id": 1} )]
    if check:
        next_num = max(check) + 1
    else:
        next_num = 1
    mon_table.insert_one( {"id": next_num, "country": f'{country}', "area": f'{area}', "population": population} )
    return "OK"


@app.put('/db/change_password', tags=['database'])
async def change_password(token: Optional[str], email, old_password, new_password):
    # MongoDB
    mon_table = mongo_db("users")
    myquery = { "email": email }
    sql_old_password = list(mon_table.find(myquery))[0]['password']
    if sql_old_password == old_password:
        # True: update new password
        myquery = {"email": email}
        newvalues = { "$set": {"password": new_password} }
        mon_table.update_one(myquery, newvalues)
        return f"帳戶: {email}, 資料已更新"
    else:
        # Tip old password error
        return "輸入的舊密碼錯誤"


@app.put('/db/modify_city_information', tags=['database'])
async def Modify_city_information(token: Optional[str], id: int,
                              country: str, area: str, population: str):
    # MongoDB
    mon_table = mongo_db("country")
    myquery = { "id": id }
    newvalues = {"$set": {"country": country, "area": area, "population": population} }
    mon_table.update_one(myquery, newvalues)
    return f"資料已更新"


@app.delete('/db/delete_user_data', tags=['database'])
async def delete_user_data(token: Optional[str] ,id: int):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    # MongoDB
    mon_table = mongo_db('db_table')
    myquery = {"id": id}
    mon_table.delete_one(myquery)
    return f"編號{id}資料已刪除"


@app.delete('/db/delete_country_data', tags=['database'], responses={404: {"model": Message}})
async def delete_country_data(token: Optional[str], id: int):
    print("id", id)
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    # MongoDB
    mon_table = mongo_db('country')
    myquery = {"id": id}
    mon_table.delete_one(myquery)
    return f"編號{id}, 資料已刪除"

@app.post("/db/search_account", tags=['database'], responses={404: {"model": Message}})
async def search_account(token: Optional[str], name: Optional[str]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    # MongoDB
    mon_table = mongo_db('db_table')
    myquery = {"Name": name}
    account = list(mon_table.find(myquery, {"_id": 0}))
    if account:
        return account
    else:
        return f"帳戶: {name}不存在"


@app.post("/db/search_id", tags=['database'])
async def search(token: Optional[str], db: Optional[str], start: Optional[int], end: Optional[int], limit: Optional[int]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)

    # MongoDB
    mon_table = mongo_db("db_table")
    result = (list(mon_table.find({}, {"_id": 0})))[start:end][:limit]
    return {"data": result}

    

@app.patch("/db/fix", tags=['database'])
async def fix(token: Optional[str], table: Optional[str] ,set_column: Optional[str],
              where_column: Optional[str], fix_to: Optional[str], target: Optional[str]):
    # MongoDB
    mon_table = mongo_db(table)
    myquery = {where_column: target}
    newvalues = {"$set": {set_column: fix_to}}
    mon_table.update_one(myquery, newvalues)

    return "Update correct"
# ---------------------------------- #

# File
# ---------------------------------- #
@app.post("/files/", tags=['files'])
async def back_file_size(token: Optional[str], file: bytes = File(...)):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    return {"file_size": len(file)}


@app.post("/upload_file/", tags=['files'])
async def upload_file(token: Optional[str], file: List[UploadFile] = File(...)):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    for file_ in file:
        contents = await file_.read()
        with open(f'./{file_.filename}', 'wb') as f:
            f.write(contents)
            f.close()
    return {"Status": 'OK'}
# ---------------------------------- #


# work_list
@app.get('/automation/webpage_test', tags=['works'])
async def browser_test(token: Optional[str]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    os.chdir('./works/Web_Work')
    os.system('python Web_test.py')
    os.chdir(Base_dir)
    return "OK"


@app.get('/automation/api_test/get/', tags=['works'])
async def api_test_get(token: Optional[str],
                       url: str = Query('http://localhost:5588/test/get', max_length=1000),
                       method: str = Query('GET', max_length=10),
                       loop: str = Query('10', max_length=100),):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    os.chdir('./works/Api_Work')
    os.system(f'start python Api_test.py {url} {method} {loop}')
    os.chdir(Base_dir)
    return "OK"


@app.post('/automation/api_test/post/', tags=['works'])
async def api_test_post(token: Optional[str],
                        url: str = Query('http://192.168.5.181:5588/test/post', max_length=1000),
                        method: str = Query('POST', max_length=10),
                        loop: str = Query('10', max_length=100),
                        message: str = Query('{"Test_Data":"Data"}', max_length=500)):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    os.chdir('./works/Api_Work')
    os.system(f'start python Api_test.py {url} {method} {loop} {message}')
    os.chdir(Base_dir)
    return result

@app.post("/cookie-and-object/", tags=['cookie'])
def create_cookie(token: Optional[str], response: Response):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}


@app.get("/commit")
def commit():
    return "OK"

@app.get("/test/get", include_in_schema=False)
def test_get():
    return {"Status": "OK"}

@app.post("/test/post", include_in_schema=False)
def test_post():
    return {"Status": "OK"}



def main():
    uvicorn.run("main:app", host="0.0.0.0", port=5588, reload=True)
