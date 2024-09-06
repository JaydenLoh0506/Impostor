# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from flask_lib import Get, APP, WebhookSend, GetPost, WebhookSend_CFE
from flask import jsonify, Response, request, render_template
from os import getenv, makedirs
from dotenv import load_dotenv
from camera_lib import CameraModule, CameraModuleEnum
from cv2 import imencode, IMREAD_COLOR, imread, imwrite
from threading import Semaphore
from face_recognition import recognize_faces
import time
from datetime import datetime
from discord import File

# load the environment variables
load_dotenv()
WEBHOOK_URL : str = str(getenv('DISCORD_WEBHOOK'))
#WEBHOOK_URL : str = str(getenv('DISCORD_WEBHOOK_TEST'))
HOST_IP : str = str(getenv('SERVER_IP'))
HOST_PORT : int = int(str(getenv('SERVER_PORT')))
CAMERAMODULE : CameraModule = CameraModule()
SEM : Semaphore = Semaphore()

CAMERAMODULE.GenerateCamDict()

# Unordered Map
UMAPCAMSENUM : dict[str, CameraModuleEnum] = {}
for cam in CameraModuleEnum:
    UMAPCAMSENUM[cam.name] = cam

UMAPCAMSMODULE: dict[str, CameraModule] = {}
for cam in CameraModuleEnum:
    UMAPCAMSMODULE[cam.value] = cam #type: ignore

# Initialize the last call time to 0
LAST_CALL_TIME = 0
        
# Centralised computing
# API Function from Server
@Get
async def Index() -> str:
    await WebhookSend(webhook_url=WEBHOOK_URL, content=f"im status {datetime.now()}")
    return f"Message Sent"

# API Function from Server
@Get
async def TestComms() -> str:
    await WebhookSend(webhook_url=WEBHOOK_URL, content=f"Comms Received Successfully {datetime.now()}")
    return "Success"

# API Function from Server
@Get
async def Test() -> str:
    cam_image : str = "image/Intruder/test.jpg"
    with open(cam_image, 'rb') as f:
        picture = File(f)
        await WebhookSend_CFE(webhook_url=WEBHOOK_URL, content=f"Intruder Detected in {1} {datetime.now()}", file = picture, embed = None)
    return "Success"

# API Function from Server
@Get
async def TestDict() -> str:
    for num, key in enumerate(CameraModuleEnum):
        CAMERAMODULE.cam_dict_[key].location_ = "Odd" if (num + 1) % 2 else "Even"
        CAMERAMODULE.cam_dict_[key].status_ = "Online" if (num + 1) % 2 else "Offline"
    await WebhookSend(webhook_url=WEBHOOK_URL, content="im cams")
    return "Changed"

# API Function from Server
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
        file = file.tobytes() #type: ignore
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + file + b"\r\n")

# API Function from Server
@Get
async def LiveList() -> str:
    return render_template("live.html")

# API Function from Server
@GetPost
async def LiveCam() -> str:
    cam_name = request.form.get('path')
    cam_name = cam_name.split(".")[1] #type: ignore
    if cam_name not in UMAPCAMSENUM:
        return "Invalid Camera"
    else:
        file = request.files["file"]
        if file.filename == "":
            return "No file selected"
        if file:
            SEM.acquire()
            file.save("image/" + UMAPCAMSENUM[cam_name].value + "/test.jpg")
            SEM.release()
            return "Frame obtained"
    return "Error"

# API Function from Server
@GetPost
async def Live(cams) -> Response | str:
    if cams not in UMAPCAMSMODULE:
        return "Invalid Camera"
    status: str = CAMERAMODULE.GetCamStat(UMAPCAMSENUM[f'{UMAPCAMSMODULE[cams]}'.split(".")[1]])
    if status == "Offline":
        return "Camera Offline"
    else:
        return Response(GetFrame(cams), mimetype="multipart/x-mixed-replace; boundary=frame")
    
def CheckTime():
    global LAST_CALL_TIME
    current_time = time.time()
    
    # Check if it has been less than 5 seconds since the last call
    if current_time - LAST_CALL_TIME < 5:
        return False
    else:
        LAST_CALL_TIME = current_time
        return True

# API Function from Server
@GetPost
async def ImpostorDetected() -> str:

    cam_no : str = UMAPCAMSENUM[request.get_json()['cam_no'].split(".")[1]].value
    if CheckTime():
        cam_image : str = "image/" + cam_no + "/test.jpg"
        intruder_image : str = "image/Intruder/test.jpg"
        image_file = imread(cam_image, IMREAD_COLOR)
        imwrite(intruder_image, image_file)
        # image = imread("image/Intruder/test.jpg", IMREAD_COLOR)
        # image : str = "image/Intruder/test.jpg"
        images = recognize_faces(intruder_image)
        print(images)
        if 'results' not in images:
            await WebhookSend(webhook_url=WEBHOOK_URL, content=f"Detected Intruder in {cam_no} failed {datetime.now()}")
            return "failed"
        

        if len(images['results']) == 0:
            await WebhookSend(webhook_url=WEBHOOK_URL, content=f"Intruder Detected in {cam_no} {datetime.now()}")
        else:
            for no, people in enumerate(images['results']):
                await WebhookSend(webhook_url=WEBHOOK_URL, content=f"{people['name']} no.{no} Detected in {cam_no}{datetime.now()}")
        with open(cam_image, 'rb') as f:
                picture = File(f)
                await WebhookSend_CFE(webhook_url=WEBHOOK_URL, content=f"@here", file = picture, embed = None)
        await WebhookSend(webhook_url=WEBHOOK_URL, content=f"im cams")
       
    return "success"

# API Function from Server
@GetPost
async def CameraSetup() -> Response | str:
    cam_enum : CameraModuleEnum | None
    cam_info : str = request.get_json()['location']
    cam_enum = CAMERAMODULE.SetCamLocation(cam_info)
    if cam_enum == None:
        return "Server full, no more cameras can be used"
    else:
        return f"{cam_enum}"
    
# API Function from Server
@GetPost
def FaceRecognition() -> Response | str:
    face_path : str = request.form.get("path") # type: ignore
    print(face_path)
    file_name : list[str] = face_path.split("/")
    name : str = file_name[-2]
    makedirs("image/faces/" + name, exist_ok=True)
    file = request.files["file"]
    if file.filename == "":
            return "No file selected"
    if file:
        SEM.acquire()
        print(file_name[1])
        file.save(face_path)
        SEM.release()
        return "Frame obtained"
    return "Error"

# API Function from Server
@GetPost
def CloseConnection() -> str:
    cam_enum : CameraModuleEnum = UMAPCAMSENUM[request.get_json()['enum'].split(".")[1]]
    CAMERAMODULE.DisableCam(cam_enum)
    return "Connection closed"

def flask_run():
    APP.run( host=HOST_IP, port=HOST_PORT)
    
def main():
    flask_run()
    
if __name__ == "__main__":
    main()
    