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
from camera_lib import ReadIP, GetCamFootage

load_dotenv()
RESTFULCLIENT : RestfulClient = RestfulClient(str(getenv('SERVER_IP')), int(str(getenv('SERVER_PORT'))))  
CONFIG_PATH: str = "client\config.txt"
CONFIG_IP: str = ReadIP(CONFIG_PATH)
#MODEL = YOLO('yolo')
            
def Test() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Test.value])
    response : str = RESTFULCLIENT.GetText(url)
    print(response)
    
def Index() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Index.value])
    response : str = RESTFULCLIENT.GetText(url)
    print(response)

def SendVideo() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.Live.value])
    video : any = GetCamFootage(CONFIG_IP)
    response : str = RESTFULCLIENT.PostFile(url, video)
    #print(response)

if __name__ == "__main__":
    #Index()
    Test()
    SendVideo()



