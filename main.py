from fastapi import FastAPI,Header
from typing import Union
import uvicorn, json
from pydantic import BaseModel
import jwt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from app.nc_json import convert_nc_json
from fastapi.middleware.cors import CORSMiddleware


f = open(r'token.json')
data = json.load(f)

SECERT_KEY = "YOUR_FAST_API_SECRET_KEY"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 800

test_user = {
   "username": "user1",
    "password": "password1",
}

app = FastAPI()

origins = {
    "http://localhost",
    "http://localhost:3000",
}

app.add_middleware(
   CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials =True,
    allow_methods = ["*"],
    allow_headers= ["*"],
)

class LoginItem(BaseModel):
    username: str
    password: str

@app.get('/')
def hello():
    return {'message': 'welcome to my FastAPI'}

@app.post("/login")
async def user_login(loginitem:LoginItem):


    data = jsonable_encoder(loginitem)

    if data['username']== test_user['username'] and data['password']== test_user['password']:

        encoded_jwt = jwt.encode(data, SECERT_KEY, algorithm=ALGORITHM)
        return {"status": "OK",
                "message": "login success",
                "token": encoded_jwt}

    else:
        return {"message":"login failed"}

@app.get('/get_index/{data_index}&{p_name}&{date}&{index_folder}')
def getGridSpei(data_index: str, index_folder: str, p_name: str, date:str = '2006-01', x_access_token: Union[list[str], None] = Header(default=None)):
    if (x_access_token != None and x_access_token[0] == data['key']):
        temp = convert_nc_json(p_name.replace('_', ' '), date, data_index, index_folder)
        return temp
    return x_access_token == data['key']
