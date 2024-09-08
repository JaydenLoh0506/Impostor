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
# Software Version : 1.0.0
# Date : 2024-08-04

from enum import Enum, unique

@unique
class CameraModuleEnum(Enum):
    cam1_ : str = "cams1"
    cam2_ : str = "cams2"
    cam3_ : str = "cams3"
    none_ : None = None
    
class CameraObject:
    def __init__(self, name: str = "", location: str = "", status: str = "") -> None:
        self.name_ : str = name
        self.location_ : str = location
        self.status_ : str = status
        
class SelfCameraObject:
    def __init__(self, *, enum : CameraModuleEnum = CameraModuleEnum.none_, object : CameraObject = CameraObject(), ip : str = "") -> None:
        self.enum_ : CameraModuleEnum = enum
        self.object_ : CameraObject = object
        self.ip_ : str = ip
        
class CameraModule:
    def __init__(self) -> None:
        # CLIENT will send self location to server
        # SERVER will assign name and status to client
        # CLIENT can request server camera dict
        self.cam_dict_ : dict[CameraModuleEnum, CameraObject] = {}

        # Client use only
        self.cam_ : SelfCameraObject = SelfCameraObject()
    
    def GenerateCamDict(self) -> None:
        """SERVER function"""
        for key in CameraModuleEnum:
            self.cam_dict_[key] = CameraObject(key.value, "", "Offline")
    
    #Read IP and Location from file
    def ReadConfig(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Initialize variables to hold IP and location
                ip_address = None
                location = None

                for line in lines:
                    line = line.strip()

                    if line.startswith("IP:"):
                        ip_address = line.split(" ")[1]
                    elif line.startswith("Location:"):
                        # Remove quotes if they exist
                        location = line.split(" ", 1)[1].strip('"')

                if ip_address is None or location is None:
                    raise ValueError("Config file is missing IP or Location entries.")
                else:
                    self.cam_.object_.location_ = location
                    self.cam_.ip_ = ip_address
                    return True

        except FileNotFoundError:
            return False
        except Exception as e:
            print(e)
            return False 
    
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

    #Set camera location (server side)
    def SetCamLocation(self, location: str) -> CameraModuleEnum | None:
        cam_enum : CameraModuleEnum = self.DistributeCam() #type: ignore
        if cam_enum != None:
            self.ToggleCamStatus(cam_enum)
            self.cam_dict_[cam_enum].location_ = location
        return cam_enum

    #Set camera to offline after use (server)
    def DisableCam(self, cam_enum: CameraModuleEnum) -> None:
        self.ToggleCamStatus(cam_enum)
        self.cam_dict_[cam_enum].location_ = ""
    