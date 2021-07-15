from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from auth import AuthHandler
from schemas import AuthDetails, DataDetails
from typing import Optional
import configparser

# config
config = configparser.ConfigParser()
config.read('config.ini')
database = config['DATABASE']
setting = config['SETTING']
# database["dbname"]

# DB
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = 'postgresql://'+database["user"]+':'+database["password"]+'@'+database["host"]+':'+database["port"]+'/'+database["dbname"]+''
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
# end DB


app = FastAPI()

# cors
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


auth_handler = AuthHandler()

@app.post('/register', status_code=201)
async def register(auth_details: AuthDetails):

    # query db select all user
    query = "SELECT * FROM users"
    result = engine.execute(query)
    users_all = list(result)
    
    if any(x['username'] == auth_details.username for x in users_all):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    
    # store in db
    query = f"INSERT INTO users (username, password) VALUES ('{auth_details.username}','{hashed_password}');"
    result = engine.execute(query)
    
    return 'USER CREATED'
    


@app.post('/login')
async def login(auth_details: AuthDetails):
    user = None

    # query db select all user
    query = "SELECT * FROM users"
    result = engine.execute(query)
    users_all = list(result)

    # check username ducplicate
    for x in users_all:
        if x['username'] == auth_details.username:
            user = x
            break
    
    # return token if login success
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return { 'token': token }

@app.get('/')
async def welcome():
    return { 'data': 'Welcome to Radiance' }

@app.get('/unprotected')
async def unprotected():
    return { 'hello': 'world' }


@app.get('/protected')
async def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }

# ######## POST and save to Database ########
# @app.post('/add')
# async def add_data(data_details: DataDetails):

#     # store in db
#     query = f"INSERT INTO data (device_id, data_smoke, data_vibration, data_mic, data_motion, data_active) VALUES ('{data_details.data_device_id}','{data_details.data_smoke}','{data_details.data_vibration}','{data_details.data_mic}','{data_details.data_motion}','1');"
#     result = engine.execute(query)

#     return { 'status': 201 }

# ######## GET data from Database ########
# @app.get('/get')
# async def get_data(username=Depends(auth_handler.auth_wrapper)):

#     # query db select 10 data
#     query = "SELECT * FROM data ORDER BY id DESC limit 10"
#     result = engine.execute(query)
#     data_10 = list(result)

#     return { 'data': data_10 }