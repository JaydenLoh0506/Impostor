# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from flask_lib import Get, APP, WebhookSend, GetPost
from flask import jsonify, Response, request, render_template
from os import getenv
from dotenv import load_dotenv
from camera_lib import CameraModule, CameraModuleEnum
from cv2 import imencode, IMREAD_COLOR, imread
from threading import Semaphore

# load the environment variables
load_dotenv()
WEBHOOK_URL : str = str(getenv('DISCORD_WEBHOOK'))
#WEBHOOK_URL : str = str(getenv('DISCORD_WEBHOOK_TEST'))
HOST_IP : str = str(getenv('SERVER_IP'))
HOST_PORT : int = int(str(getenv('SERVER_PORT')))
CAMERAMODULE : CameraModule = CameraModule()
SEM : Semaphore = Semaphore()

CAMERAMODULE.GenerateCamDict()

# unordered map
CAMS_MAP : dict[str, CameraModuleEnum] = {}
for key in CameraModuleEnum:
    CAMS_MAP[key.value] = key

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

def GetFrame(path: str):
    while True:
        SEM.acquire()
        file = imread("image/" + path + "/test.jpg", IMREAD_COLOR)
        SEM.release()
        _b, file = imencode(".jpg", file)
        file = file.tobytes()
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + file + b"\r\n")

@Get # temporary code
def LiveList() -> str:
    temp : str = ""
    for f in range(1, 4):
        temp += f'<a href="/live/cams{f}">cams{f}</a><br>'
    return temp

@GetPost
def LiveCam() -> Response:
    cam_name = request.form.get('path')
    if cam_name not in CAMS_MAP:
        return "Invalid Camera"
    else:
        file = request.files["file"]
        if file.filename == "":
            return "No file selected"
        if file:
            SEM.acquire()
            file.save("image/" + cam_name + "/test.jpg")
            SEM.release()
            return "Frame obtained"

@GetPost
def Live(cams) -> Response:
    # print(CAMERAMODULE.ReturnEnum(cams))
    status: str = CAMERAMODULE.GetCamStat(CAMERAMODULE.ReturnEnum(cams))
    if cams not in CAMS_MAP:
        return "Invalid Camera"
    if status == "Offline":
        return "Camera Offline"
    else:
        return Response(GetFrame(cams), mimetype="multipart/x-mixed-replace; boundary=frame")


@GetPost
def CameraSetup() -> Response:
    cam_enum : CameraModuleEnum | None
    cam_info = request.get_json()
    cam_enum = CAMERAMODULE.SetCamLocation(cam_info)
    if cam_enum == None:
        return "Server full, no more cameras can be used"
    else:
        return f"{cam_enum}"

@GetPost
def CloseConnection() -> str:
    cam_enum : CameraModuleEnum = CAMERAMODULE.ReturnEnum(request.get_json())
    CAMERAMODULE.DisableCam(cam_enum)
    return "Connection closed"

def flask_run():
    APP.run( host=HOST_IP, port=HOST_PORT)
    
def main():
    flask_run()
    #Live()
    
if __name__ == "__main__":
    main()
    