# include this file at the top of your main file

# [WARNING] Update Service Dict requires try and except block

# this file is a library for client requests
# it includes functions for client requests

# Functions
# - PostJson : Post Json Function
# - PostGetJson : Post Json and Get Json Function
# - GetJson : Get Json Function
# - GetText : Get Text Function
# - PostFile : Post File Function
# - GetFile : Get File Function

# Variables naming convention
# - GLOBAL_VARIABLE
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

# Python Version : Python 3.12.1
# Date : 2024-07-07
# Requests Version : 2.32.3
# Software version : 0.1.3

# arguments rules
# json_dict : dict[str, str]

# To Run this file
# pip install requests
# import this file in your main file

from requests import post, Response, get # type: ignore
from enum import Enum, unique   

# Enum for API Service must match the server
@unique # ignore type convention due to enum using VariableName
class ApiServiceEnum(Enum):
    ApiService = "ApiService"
    Index = "Index"
    Test = "Test"
    TestComms = "TestComms"
    Live = "Live"

API_SERVICE_DICT : dict[ApiServiceEnum, tuple[bool,str]]
API_SERVICE_DICT = {
    ApiServiceEnum.ApiService : (False,"Offered Service"),
    ApiServiceEnum.Index : (True,"Main Web"),
    ApiServiceEnum.Test : (False,"Internal Verification"),
    ApiServiceEnum.TestComms : (True,"Test Server Communication"),
    ApiServiceEnum.Live : (False,"Live Cam")
}

class RestfulClient:
    # Constructor
    def __init__(self, server_ip : str, server_port : int) -> None:
        self.server_ip_ : str = server_ip
        self.server_port_ : int = server_port
        self.service_dict_ : dict[str, str]
        self.server_api_ : bool = False
        #self.UpdateServiceDict() Can crash if server is not running
        
    # SETTERS
    def UpdateServerIp(self, server_ip : str) -> None:
        self.server_ip_ = server_ip
        
    def UpdateServerPort(self, server_port : int) -> None:
        self.server_port_ = server_port 
        
    def CreateUrl(self, route : str) -> str:
        return "http://" + self.server_ip_ + ":" + str(self.server_port_) + route

    # Post Json Function and Get Text Response
    def PostJson(self, url : str, json_dict : dict[str, str]) -> str:
        response : Response = post(url=url, json=json_dict)
        return response.text()

    # Post Json and Get Json Response
    def PostGetJson(self, url : str, json_dict : dict[str, str]) -> dict[str, str]:
        response : Response = post(url=url, json=json_dict)
        return response.json()

    # Get Json Response
    def GetJson(self, url : str) -> dict[str, str]:
        response : Response = get(url=url)
        return response.json()

    # Get Text Response
    def GetText(self, url : str) -> str:
        response : Response = get(url=url)
        return response.text

    # Post File Function
    def PostFile(self, url : str, file) -> str:
        response : Response = post(url=url, files={"file": file})
        return response.text

    # Get File Function
    def GetFile(self, url : str) -> str:
        response : Response = get(url=url)
        return response.text
    
    # Update Service Dict
    def UpdateServiceDict(self) -> None:
        """Require try and except block"""
        self.service_dict_ = self.GetJson(self.CreateUrl("/api")) # First Route must be /api is fixed