# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from os import getenv
from dotenv import load_dotenv
from responses_lib import RestfulClient, ApiServiceEnum
from camera_lib import CameraModule, CameraModuleEnum
from cv2 import VideoCapture, UMat, imencode, imshow, waitKey, destroyAllWindows
from cv2.typing import MatLike
from sys import exit

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
        #print(e)
        exit("Server is offline")

#Set camera IP and location
def CameraSetup() -> None:
    if CAMERA_MODULE.read_config(CONFIG_PATH):
        print("Camera IP and Location obtained")
        url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.CameraSetup.value])
        response : str = RESTFULCLIENT.PostCam(url, CAMERA_MODULE.cam_[1].location_)
        cam_enum : CameraModuleEnum = CAMERA_MODULE.ReturnEnum(response)
        CAMERA_MODULE.cam_[0] = cam_enum
        CAMERA_MODULE.cam_[1].name_ = cam_enum.value
        CAMERA_MODULE.cam_[1].status = "Online"
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

def SendVideo() -> None:
    # url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Live.value + '/' + CAMERA_MODULE.cam_[1].name_])
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.LiveCam.value])
    #video : any = CAMERA_MODULE.GetCamFootage(CAMERA_MODULE.cam_[2])
    camera : VideoCapture = VideoCapture(CAMERA_MODULE.cam_[2])
    success : bool
    frame : UMat | MatLike
    ret : bool
    #video = None
    #cam_name : str = RESTFULCLIENT.PostCam(url, f'{CAMERA_MODULE.cam_[1].name_}')
    #print(cam_name)
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to read frame")
            break
        else:
            # imshow('Webcam', frame)
            ret, buffer = imencode(".jpg", frame)
            video = buffer.tobytes()
            response : str = RESTFULCLIENT.PostFile(url, CAMERA_MODULE.cam_[1].name_, video)
            print(response)
    # response : str = RESTFULCLIENT.PostCam(url, 'test')
            #print("Sending")

def CloseConnection() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.CloseConnection.value])
    response : str = RESTFULCLIENT.PostCam(url, f'{CAMERA_MODULE.cam_[0]}')
    print(response)

# def SendVideo() -> None:
#     url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Live.value])
#     video : any = GetCamFootage(CONFIG_IP)
#     response : str = RESTFULCLIENT.PostFile(url, video)
    #print(response)

if __name__ == "__main__":
    ServerStatus()
    CameraSetup()
    #Index()
    #Test()
    SendVideo()
    CloseConnection()



