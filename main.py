from settings import *

Base_dir = os.getcwd()
vip_token = 'efai_token_apikey_2021_'

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

@app.get("/get_token/", tags=['Token'])
async def get_token(x_api_key: Optional[str]):
    global x_api_token
    if x_api_key == vip_token:
        x_api_token = identity_generator()
        t = Timer(14400.0, reset_token)
        t.start()
        return {"token": x_api_token}
    else:
        Message = {"Status": "Error", "Message": "x_api_key is error"}
        return JSONResponse(status_code=404, content=Message)


@app.get("/views_users/", tags=["database"])
async def get_users(token: Optional[str]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    cursor.execute('SELECT * FROM `db_table`')
    data = cursor.fetchall()
    return {"User_data": data}


@app.get("/views_country/", tags=['database'])
async def get_country(token: Optional[str]):
    cursor.execute('SELECT * FROM `country`')
    data = cursor.fetchall()
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    return {"Country": data}

# db
# ---------------------------------- #
@app.post('/db/insert_user_data', tags=['database'])
async def insert(token: Optional[str], name: Optional[str], age: Optional[int],
                 feature: Optional[str], level: Optional[int]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    sql = "insert into db_table(Name, Age, Feature, Level) values(%s, %s, %s, %s)"
    cursor.execute(sql, (name, age, feature, level))
    db.commit()
    return "OK"


@app.post('/db/insert_country_data', tags=['database'])
async def insert(token: Optional[str], country: Optional[str],
                 area: Optional[str], population: Optional[int]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    sql = "insert into country(country, area, population) values(%s, %s, %s)"
    cursor.execute(sql, (country, area, population))
    db.commit()
    return "OK"


@app.post("/db/search_account", tags=['database'], responses={404: {"model": Message}})
async def search_account(token: Optional[str], account: Optional[str]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    cursor.execute("SELECT * FROM `db_table`")
    data = cursor.fetchall()
    inside = False
    for n in data:
        if account in n:
            inside = True
            continue
    if not inside:
        Message = {"Status": "Error", "Message": "Account is not Found"}
        return JSONResponse(status_code=404, content=Message)
    else:
        return data


@app.post("/db/search_id", tags=['database'])
async def search(token: Optional[str], start: Optional[int], end: Optional[int], limit: Optional[int]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    if limit:
        cursor.execute("select * from country limit %s, %s", (start, end))
    else:
        cursor.execute("select * from db_table")
    data = cursor.fetchall()
    return data[:limit]
    # return data[start:end]

@app.patch("/db/fix", tags=['database'])
async def fix(token: Optional[str], table: Optional[str] ,columns: Optional[str],
              target: Optional[str], fix_to: Optional[str]):
#     cursor.execute(f'UPDATE `{table}` SET `{columns}`="{fix_to}" WHERE `{columns}`="{target}"')
    cursor.execute("update %s set %s = %s where %s = %s", (table, columns, fix_to, columns, target))
    db.commit()
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
                       url: str = Query('http://localhost:8000/test/', max_length=1000),
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
                        url: str = Query('http://localhost:8000/test/', max_length=1000),
                        method: str = Query('POST', max_length=10),
                        loop: str = Query('10', max_length=100),
                        message: str = Query('{"Test_Data":"Data"}', max_length=500)):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    os.chdir('./works/Api_Work')
    os.system(f'start python Api_test.py {url} {method} {loop}')
    os.chdir(Base_dir)
    return "OK"


@app.get('/automation/android_app', tags=['works'])
async def android_app(token: Optional[str]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    os.system('')
    return "OK"


@app.get('/automation/android_browser', tags=['works'])
async def android_browser(token: Optional[str]):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    os.system('')
    return "OK"

# ---------------------------------- #

@app.post("/cookie-and-boject/", tags=['cookie'])
def create_cookie(token: Optional[str], response: Response):
    if token != x_api_token:
        Message = {"Status": "Error", "Message": "Token is error"}
        return JSONResponse(status_code=404, content=Message)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=5588, reload=True)
