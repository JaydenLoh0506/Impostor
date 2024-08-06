# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

import sys
from os import getenv
from dotenv import load_dotenv
from responses_lib import RestfulClient, ApiServiceEnum
from camera_lib import CameraModule

load_dotenv()
RESTFULCLIENT : RestfulClient = RestfulClient(str(getenv('SERVER_IP')), int(str(getenv('SERVER_PORT'))))  
CAMERA_MODULE : CameraModule = CameraModule()
CONFIG_PATH: str = "config.txt"
#CONFIG_IP: str = ReadIP(CONFIG_PATH)
#MODEL = YOLO('yolo')

#Check server status
def ServerStatus() -> None:
    try:
        if not RESTFULCLIENT.server_api_:
            RESTFULCLIENT.UpdateServiceDict()
            RESTFULCLIENT.server_api_ = True
    except Exception as e:
        print(e)
        sys.exit("Server is offline")

#Set camera IP and location
def CameraLocation() -> None:
    if CAMERA_MODULE.read_config(CONFIG_PATH):
        print("Camera IP and Location obtained")
        #print(CAMERA_MODULE.cam_[1].location_)
        #data : dict[str, list[str]] = {'cam_info' : CAMERA_MODULE.cam_}
        url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.CameraLocation.value])
        response : str = RESTFULCLIENT.PostCam(url, CAMERA_MODULE.cam_[1].location_)
        print(response)
    else:
        print("Failed to get IP and Location")
            
def Test() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Test.value])
    response : str = RESTFULCLIENT.GetText(url)
    print(response)
    
def Index() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Index.value])
    response : str = RESTFULCLIENT.GetText(url)
    print(response)


# def SendVideo() -> None:
#     url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Live.value])
#     video : any = GetCamFootage(CONFIG_IP)
#     response : str = RESTFULCLIENT.PostFile(url, video)
    #print(response)

if __name__ == "__main__":
    ServerStatus()
    CameraLocation()
    #Index()
    #Test()
    #SendVideo()



