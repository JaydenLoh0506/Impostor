# include this file at the top of your main file

# this file is a library for flask
# it includes decorators for flask
# this file will run as the server

# Decorators
# - Callback : Generic Function
# - Get : Get Function
# - Post : Post Function
# - GetPost : Get and Post Function

# Python Version : Python 3.12.1
# Date : 21-07-2024
# Flask Version : 3.0.3
# Software version : 0.1.1

# To Run this file
# You need to install Flask
# pip install Flask
# APP.run() will run the server

from flask import Flask, jsonify, Response, request
from functools import wraps
from enum import Enum, unique
from aiohttp import ClientSession
from discord import Webhook, Embed, File


# Registry for Route to Enum
@unique # ignore type convention due to enum using VariableName
class CallbackFunctionRoute(Enum):
    ApiService = "/api"
    Index = "/"
    Test = "/test"
    TestComms = "/testcomms"
    LiveList = "/live"
    Live = "/live/<cams>"
    LiveCam = "/livecam"
    CamDict = "/camdict"
    TestDict = "/testdict"
    CameraSetup = "/camerasetup"
    CloseConnection = "/closeconnection"

# dict[function_name, route]
CALLBACK_FUNCTION_ROUTE : dict[str, str] = {i.name : i.value for i in CallbackFunctionRoute}
APP : Flask = Flask(__name__, template_folder="templates")

# Decorator
# Generic Function
def Callback(func):
    @APP.route(CALLBACK_FUNCTION_ROUTE[func.__name__])
    @wraps(func)
    def Wrapper(*args : any, **kwargs : any):
        return APP.ensure_sync(func)(*args, **kwargs)
        #return func(*args, **kwargs)
    return Wrapper

# Get Function
def Get(func):  
    @APP.route(CALLBACK_FUNCTION_ROUTE[func.__name__], methods=["GET"])
    @wraps(func)
    def Wrapper(*args : any, **kwargs : any):
        return APP.ensure_sync(func)(*args, **kwargs)
        #return func(*args, **kwargs)
    return Wrapper

# Post Function
def Post(func):
    @APP.route(CALLBACK_FUNCTION_ROUTE[func.__name__], methods=["POST"])
    @wraps(func)
    def Wrapper(*args : any, **kwargs : any):
        return APP.ensure_sync(func)(*args, **kwargs)
        #return func(*args, **kwargs)
    return Wrapper

# Get and Post Function
def GetPost(func):
    @APP.route(CALLBACK_FUNCTION_ROUTE[func.__name__], methods=["GET", "POST"])
    @wraps(func)
    def Wrapper(*args : any, **kwargs : any):
        return APP.ensure_sync(func)(*args, **kwargs)
        #return func(*args, **kwargs)
    return Wrapper

# Webhook
async def WebhookSend_CFE(webhook_url : str, *, content : str, file : File, embed : Embed) -> None:
    async with ClientSession() as session:
        WEBHOOK = Webhook.from_url(webhook_url, session=session)
        await WEBHOOK.send(content=content, file=file, embed=embed)

async def WebhookSend(webhook_url : str, *, content : str) -> None:
    async with ClientSession() as session:
        WEBHOOK = Webhook.from_url(webhook_url, session=session)
        await WEBHOOK.send(content=content)
        
# Service Functions
@Get 
def ApiService() -> Response:
    return jsonify(CALLBACK_FUNCTION_ROUTE)