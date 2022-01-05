import uvicorn
from typing import Optional, Set, List
from fastapi import FastAPI, File, UploadFile, Path,\
                    HTTPException, Query, Header,  \
                    Response, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from pydantic import BaseModel, Field
import secrets
from threading import Timer
from package.generate import identity_generator
import MySQLdb
import os

# def database():
#     db = MySQLdb.connect(host='localhost',
#                          user='rubio',
#                          password='0000',
#                          db='api_db',
#                          charset='utf8')
#     cursor = db.cursor()
#     return db, cursor

# db, cursor = database()


def mongo_db(table):
    with open('./password.json', mode='r') as f:
        data = json.load(f)
        client = MongoClient(f"mongodb+srv://{data['Account']}:{data['Password']}@cluster1.kvjio.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mon_db = client['api_db']
        mon_table = mon_db[table]
        return mon_table
