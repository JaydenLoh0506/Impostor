# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from flask_lib import Get, APP, WebhookSend, GetPost
from flask import jsonify, Response, request, render_template
from os import getenv, makedirs
from dotenv import load_dotenv
from camera_lib import CameraModule, CameraModuleEnum
from cv2 import imencode, IMREAD_COLOR, imread, imwrite
from threading import Semaphore
from face_recognition import recognize_faces
import time

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
UMAPCAMS : dict[str, CameraModuleEnum] = {}
for cam in CameraModuleEnum:
    UMAPCAMS[cam.name] = cam

UMAPCAMS2: dict[str, CameraModule] = {}
for cam in CameraModuleEnum:
    UMAPCAMS2[cam.value] = cam #type: ignore

# Initialize the last call time to 0
LAST_CALL_TIME = 0
        
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
        file = file.tobytes() #type: ignore
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + file + b"\r\n")

@Get # temporary code
def LiveList() -> str:
    temp : str = ""
    for f in range(1, 4):
        temp += f'<a href="/live/cams{f}">cams{f}</a><br>'
    return render_template("live.html")

@GetPost
def LiveCam() -> str:
    cam_name = request.form.get('path')
    cam_name = cam_name.split(".")[1] #type: ignore
    if cam_name not in UMAPCAMS:
        return "Invalid Camera"
    else:
        file = request.files["file"]
        if file.filename == "":
            return "No file selected"
        if file:
            SEM.acquire()
            file.save("image/" + UMAPCAMS[cam_name].value + "/test.jpg")
            SEM.release()
            return "Frame obtained"
    return "Error"

@GetPost
def Live(cams) -> Response | str:
    if cams not in UMAPCAMS2:
        return "Invalid Camera"
    status: str = CAMERAMODULE.GetCamStat(UMAPCAMS[f'{UMAPCAMS2[cams]}'.split(".")[1]])
    if status == "Offline":
        return "Camera Offline"
    else:
        return Response(GetFrame(cams), mimetype="multipart/x-mixed-replace; boundary=frame")
    
def check_time():
    global LAST_CALL_TIME
    current_time = time.time()
    
    # Check if it has been less than 10 seconds since the last call
    if current_time - LAST_CALL_TIME < 10:
        return False
    else:
        LAST_CALL_TIME = current_time
        return True

@GetPost
def ImpostorDetected() -> str:
    cam_no : str = UMAPCAMS[request.get_json()['cam_no'].split(".")[1]].value
    if check_time():
        cam_image : str = "image/" + cam_no + "/test.jpg"
        intruder_image : str = "image/Intruder/test.jpg"
        image = imread(cam_image, IMREAD_COLOR)
        imwrite(intruder_image, image)
        # image = imread("image/Intruder/test.jpg", IMREAD_COLOR)
        # image : str = "image/Intruder/test.jpg"
        print(recognize_faces(intruder_image))
    return "success"


@GetPost
def CameraSetup() -> Response | str:
    cam_enum : CameraModuleEnum | None
    cam_info : str = request.get_json()['location']
    cam_enum = CAMERAMODULE.SetCamLocation(cam_info)
    if cam_enum == None:
        return "Server full, no more cameras can be used"
    else:
        return f"{cam_enum}"
    
@GetPost
def FaceRecognition() -> Response | str:
    face_path : str = request.form.get("path") # type: ignore
    file_name : list[str] = (face_path.split("image/", 1)[1]).split("/")
    name : str = file_name[0]
    makedirs("image/" + name, exist_ok=True)
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

@GetPost
def CloseConnection() -> str:
    cam_enum : CameraModuleEnum = UMAPCAMS[request.get_json()['enum'].split(".")[1]]
    CAMERAMODULE.DisableCam(cam_enum)
    return "Connection closed"

def flask_run():
    APP.run( host=HOST_IP, port=HOST_PORT)
    
def main():
    flask_run()
    
if __name__ == "__main__":
    main()
    