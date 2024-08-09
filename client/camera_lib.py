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
from cv2 import VideoCapture, UMat, imencode, imshow, waitKey, destroyAllWindows
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
        
class SelfCameraObject:
    def __init__(self, *, enum : CameraModuleEnum, object : CameraObject, ip : str) -> None:
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
        self.cam_ : SelfCameraObject
    
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
                for line in file:
                    line = line.strip()
                    # Extract the IP address from the content
                    if line.startswith("IP:"):
                        self.cam_.ip_ = line.split(" ")[1]
                        break
                return True
        except FileNotFoundError:
            return False
        except Exception as e:
            return False
        
    def read_config(self, file_path):
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
                    
                self.cam_.ip_ = new_ip
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

    def SetCamLocation(self, location: str) -> CameraModuleEnum | None:
        cam_enum : CameraModuleEnum = self.DistributeCam() #type: ignore
        if cam_enum != None:
            self.ToggleCamStatus(cam_enum)
            self.cam_dict_[cam_enum].location_ = location
        return cam_enum

    def DisableCam(self, cam_enum: CameraModuleEnum) -> None:
        self.ToggleCamStatus(cam_enum)
        self.cam_dict_[cam_enum].location_ = ""

    # def ReturnEnum(self, cam_enum_str: str) -> CameraModuleEnum | None:
    #     cam_enum  : CameraModuleEnum | None = None
    #     for key in CameraModuleEnum:
    #         if f'{key.value}' == cam_enum_str or f'{key}' == cam_enum_str:
    #             cam_enum = key
    #             break
    #     return cam_enum
    