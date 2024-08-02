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
from cam_ip_lib import ReadIP
from cv2 import VideoCapture, UMat, imencode
from cv2.typing import MatLike

load_dotenv()
RESTFULCLIENT : RestfulClient = RestfulClient(str(getenv('SERVER_IP')), int(str(getenv('SERVER_PORT'))))  
CONFIG_PATH: str = "client\config.txt"
CONFIG_IP: str = ReadIP(CONFIG_PATH)
#MODEL = YOLO('yolo')
            
def Test2() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Test2.value])
    response : str = RESTFULCLIENT.GetText(url)
    print(response)
    
def Index() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Index.value])
    response : str = RESTFULCLIENT.GetText(url)
    print(response)

def SendVideo() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Live.value])
    camera : VideoCapture = VideoCapture(CONFIG_IP)
    success : bool
    frame : UMat | MatLike
    ret : bool
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to read frame")
            break
        else:
            ret, buffer = imencode(".jpg", frame)
            image = buffer.tobytes()
            response : str = RESTFULCLIENT.PostFile(url, image)
    #print(response)

if __name__ == "__main__":
    #Index()
    Test2()
    SendVideo()



