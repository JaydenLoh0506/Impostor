# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from flask_lib import Get, APP, WebhookSend, GetPost
from flask import jsonify, Response, request
from os import getenv
from dotenv import load_dotenv
from camera_lib import CameraModule, CameraModuleEnum
from sys import stderr  # remove this line


# load the environment variables
load_dotenv()
WEBHOOK_URL : str = str(getenv('DISCORD_WEBHOOK'))
#WEBHOOK_URL : str = str(getenv('DISCORD_WEBHOOK_TEST'))
HOST_IP : str = str(getenv('SERVER_IP'))
HOST_PORT : int = int(str(getenv('SERVER_PORT')))
CAMERAMODULE : CameraModule = CameraModule()

CAMERAMODULE.GenerateCamDict()

# unordered map
CAMS_MAP : dict[str, CameraModuleEnum] = {}
for key in CameraModuleEnum:
    CAMS_MAP[key.name] = key

# Centralised computing
@Get
async def Index() -> str:
    await WebhookSend(webhook_url=WEBHOOK_URL, content="im status")
    return f"Message Sent"

@Get
async def TestComms() -> str:
    await WebhookSend(webhook_url=WEBHOOK_URL, content="Comms Received Successfully")
    return "Success"

# Will be removed
@Get
async def Test() -> str:
    return "Success"

@Get
async def TestDict() -> str:
    for num, key in enumerate(CameraModuleEnum):
        CAMERAMODULE.cam_dict_[key].location_ = "Odd" if (num + 1) % 2 else "Even"
        CAMERAMODULE.cam_dict_[key].status_ = "Online" if (num + 1) % 2 else "Offline"
    await WebhookSend(webhook_url=WEBHOOK_URL, content="im cams")
    return "Changed"

@Get
async def CamDict() -> Response:
    json_dict : dict[str, dict[str, str]] = {}
    for key, value in CAMERAMODULE.cam_dict_.items():
        json_dict[key.name] = {
            "name" : value.name_,
            "location" : value.location_,
            "status" : value.status_
        }
    return jsonify(json_dict)

def GetFrame():
    while True:
        file = request.files["file"]
        if file.filename == "":
            return "No file selected"
        if file:
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + file + b"\r\n")
            
@Get # temporary code
def LiveList() -> str:
    temp : str = ""
    for f in range(1, 4):
        temp += f'<a href="/live/cams{f}">cams{f}</a><br>'
    return temp

@Get # temporary code
def Live(cams) -> str:
    if cams not in CAMS_MAP:
        return "Invalid Camera"
    print(CAMS_MAP[cams], file=stderr)
    return cams

@GetPost
def CameraLocation() -> Response:
    cam_info = request.get_json()
    print(cam_info)
    return "Cam Info obtained"

def flask_run():
    APP.run( host=HOST_IP, port=HOST_PORT)
    
def main():
    flask_run()
    #Live()
    
if __name__ == "__main__":
    main()
    