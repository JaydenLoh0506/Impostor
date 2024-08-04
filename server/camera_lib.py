# this file can be run on client and server

# Server 
# run GenerateCamDict
# let client update server dict with location and server assign enum, name and status

# Client
# client store cam_ip

# Class 
# - CameraModuleEnum : Enum for Camera Module
# - CameraObject : Camera Object
# - CameraModule : Camera Module

# Functions 
# - GetImagePath : Get path to save images for specific camera
# - GetCamStat : Get camera status
# - DistributeCam : Get camera with "Offline" status
# - ToggleCamStatus : Toggle camera status
# - GetCamFootage : Get camera footage
# - ReadIP : Get camera IP
# - ChangeIP : Change camera IP

# Python Version : Python 3.12.1
# Date : 2024-08-04

from enum import Enum, unique
from cv2 import VideoCapture, UMat, imencode
from cv2.typing import MatLike

@unique
class CameraModuleEnum(Enum):
    cam1_ : str = "cams1"
    cam2_ : str = "cams2"
    cam3_ : str = "cams3"
    
class CameraObject:
    def __init__(self, name: str = "", location: str = "", status: str = "") -> None:
        self.name_ : str = name
        self.location_ : str = location
        self.status_ : str = status

class CameraModule:
    def __init__(self) -> None:
        # CLIENT will send self location to server
        # SERVER will assign name and status to client
        # CLIENT can request server camera dict
        self.cam_dict_ : dict[CameraModuleEnum, CameraObject] = {}

        # Client use only
        self.cam_ : tuple[CameraModuleEnum, CameraObject, str]
    
    def GenerateCamDict(self) -> None:
        """SERVER function"""
        for key in CameraModuleEnum:
            self.cam_dict_[key] = CameraObject(key.value, "", "Offline")
    
    #Get camera IP
    def ReadIP(self, file_path) -> bool:
        """CLIENT function"""
        try:
            with open(file_path, 'r') as file:
                # Read the content of the file
                content = file.readline().strip()
                
                # Extract the IP address from the content
                if content.startswith("IP:"):
                    self.cam_[2] = content.split(" ")[1]
                    return True
                else:
                    raise ValueError("Invalid file format. Expected 'IP: <url>'.")
        except FileNotFoundError:
            return False
        except Exception as e:
            return False

    #Change camera IP
    def ChangeIP(self, file_path : str, new_ip : str):
        """CLIENT function"""
        try:
            # Ensure the new IP ends with /video
            if not new_ip.endswith("/video"):
                new_ip += "/video"
                
            # Read the current content of the file
            with open(file_path, 'r') as file:
                content = file.readline().strip()
            
            # Modify the content with the new IP address
            if content.startswith("IP:"):
                prefix = content.split(" ")[0]
                new_content = f"{prefix} {new_ip}"
                
                # Write the updated content back to the file
                with open(file_path, 'w') as file:
                    file.write(new_content)
                    
                self.cam_[2] = new_ip
            else:
                raise ValueError("Invalid file format. Expected 'IP: <url>'.")
        except FileNotFoundError:
            return "The file does not exist."
        except Exception as e:
            return f"An error occurred: {str(e)}"
        
    
     # SERVER function
    #Get path to save images for specific camera
    def GetImagePath(self, cams : CameraModuleEnum) -> str:
        """SERVER function"""
        return "image/" + self.cam_dict_[cams].name_
    
    #Get camera status
    def GetCamStat(self, cams : CameraModuleEnum) -> str:
        """SERVER function"""
        return self.cam_dict_[cams].status_
    
    #Get camera with "Offline" status
    def DistributeCam(self) -> CameraModuleEnum | None:
        """SERVER function"""
        for key, value in self.cam_dict_.items():
            if value.status_ == "Offline":
                return key
        return None
    
    #Toggle camera status
    def ToggleCamStatus(self, cams: CameraModuleEnum) -> None:
        """SERVER function"""
        if self.cam_dict_[cams].status_ == "Offline":
            self.cam_dict_[cams].status_ = "Online"
        else:
            self.cam_dict_[cams].status_ = "Offline"

    #Get camera footage
    def GetCamFootage(self, source: str) -> any:
        """SERVER function"""
        camera : VideoCapture = VideoCapture(source)
        success : bool
        frame : UMat | MatLike
        ret : bool
        video = None
        while True:
            success, frame = camera.read()
            if not success:
                print("Failed to read frame")
                break
            else:
                ret, buffer = imencode(".jpg", frame)
                video = buffer.tobytes()
                return video
        return video
    