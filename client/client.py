# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

import signal
import cv2
from os import getenv
from dotenv import load_dotenv
from responses_lib import RestfulClient, ApiServiceEnum
from camera_lib import CameraModule, CameraModuleEnum, SelfCameraObject
from cv2.typing import MatLike
from ultralytics import YOLO # type: ignore
from math import ceil
from sys import exit

load_dotenv()
RESTFULCLIENT : RestfulClient = RestfulClient(str(getenv('SERVER_IP')), int(str(getenv('SERVER_PORT'))))  
CAMERA_MODULE : CameraModule = CameraModule()
MODEL = YOLO('yolov8n.pt')
# MODEL.classes = [0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

CONFIG_PATH: str = "config.txt"

# Unordered Map
UMAPCAMS : dict[str, CameraModuleEnum] = {}
for cam in CameraModuleEnum:
    UMAPCAMS[cam.name] = cam

UMAPCAMS2: dict[str, CameraModule] = {}
for cam in CameraModuleEnum:
    UMAPCAMS2[cam.value] = cam #type : ignore

#Check server status
def ServerStatus() -> None:
    try:
        if not RESTFULCLIENT.server_api_:
            RESTFULCLIENT.UpdateServiceDict()
            RESTFULCLIENT.server_api_ = True
    except Exception as e:
        exit("Server is offline")

#Set camera IP and location
def CameraSetup() -> None:
    if CAMERA_MODULE.read_config(CONFIG_PATH):
        print("Camera IP and Location obtained")
        url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.CameraSetup.value])
        temp_dict : dict[str, str] = {'location': f'{CAMERA_MODULE.cam_.object_.location_}'}
        response : str = RESTFULCLIENT.PostJson(url, temp_dict)
        response = response.split(".")[1]
        cam_enum : CameraModuleEnum = UMAPCAMS[response]
        CAMERA_MODULE.cam_.enum_ = cam_enum
        CAMERA_MODULE.cam_.object_.name_ = cam_enum.value
        CAMERA_MODULE.cam_.object_.status_ = "Online"
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
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.LiveCam.value])
    camera : cv2.VideoCapture = cv2.VideoCapture(CAMERA_MODULE.cam_.ip_)
    success : bool
    frame : cv2.UMat | MatLike
    ret : bool
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to read frame")
            break
        else:
            results = Detection(frame)
            # print(type(results))
            # results = squeeze(results.render())
            ret, buffer = cv2.imencode(".jpg", results)
            video = buffer.tobytes()
            response : str = RESTFULCLIENT.PostFile(url, CAMERA_MODULE.cam_.enum_, video)
            print(response)


def Detection(frame):

    # classNames = ['person', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe']
    # classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    #           "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    #           "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    #           "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
    #           "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    #           "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
    #           "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
    #           "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
    #           "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    #           "teddy bear", "hair drier", "toothbrush"
    #           ]
    results = MODEL(frame, stream = False)
    for result in results:
        boxes = result.boxes

        for box in boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Extract the class and confidence
            cls = int(box.cls[0])
            confidence = box.conf[0]

            # Get the class name
            class_name = MODEL.names[cls]

            # Draw bounding box and label on the frame
            label = f'{class_name}: {confidence:.2f}'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    # coordinates
    # for r in results:
    #     boxes = r.boxes

    #     for box in boxes:
    #         # bounding box
    #         x1, y1, x2, y2 = box.xyxy[0]
    #         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

    #         # put box in cam
    #         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

    #         # confidence
    #         confidence = ceil((box.conf[0]*100))/100
    #         print("Confidence --->",confidence)

    #         # class name
    #         cls = int(box.cls[0])
    #         print("Class name -->", classNames[cls])

    #         # object details
    #         org = [x1, y1]
    #         font = cv2.FONT_HERSHEY_SIMPLEX
    #         fontScale = 1
    #         color = (255, 0, 0)
    #         thickness = 2

    #         cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)
    return frame

def CloseConnection() -> None:
    url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_[ApiServiceEnum.CloseConnection.value])
    temp_dict : dict[str, str] = {'enum' : f'{CAMERA_MODULE.cam_.enum_}'}
    response : str = RESTFULCLIENT.PostJson(url, temp_dict)
    print(response)

def SignalHandler(sig, frame) -> None:
    CloseConnection()
    exit()

signal.signal(signal.SIGINT, SignalHandler)

if __name__ == "__main__":
    ServerStatus()
    CameraSetup()
    #Index()
    #Test()
    SendVideo()
    CloseConnection()



