from enum import Enum, unique
from cv2 import VideoCapture, UMat, imencode
from cv2.typing import MatLike

@unique
class CameraModuleEnum(Enum):
    cam1_ : str = "cams1"
    cam2_ : str = "cams2"
    cam3_ : str = "cams3"

CAM_PATH_DICT : dict[CameraModuleEnum, str]
CAM_PATH_DICT = {
    CameraModuleEnum.cam1_ : "image/cams1",
    CameraModuleEnum.cam2_ : "image/cams2",
    CameraModuleEnum.cam3_ : "image/cams3"
}

CAM_LOC_DICT : dict[CameraModuleEnum, str]
CAM_LOC_DICT = {
    CameraModuleEnum.cam1_ : "sky",
    CameraModuleEnum.cam2_ : "door",
    CameraModuleEnum.cam3_ : "fence"
}

CAM_STAT_DICT : dict[CameraModuleEnum, str]
CAM_STAT_DICT  = {
    CameraModuleEnum.cam1_ : "Offline",
    CameraModuleEnum.cam2_ : "Offline",
    CameraModuleEnum.cam3_ : "Offline"
}

class CameraModule:
    def __init__(self) -> None:
        pass

    #Get path to save images for specific camera
    def GetImagePath(self, cams : CameraModuleEnum) -> str:
        return CAM_PATH_DICT[cams]
    
    #Get camera status
    def GetCamStat(self, cams : CameraModuleEnum) -> str:
        return CAM_STAT_DICT[cams]
    
    #Get camera with "Offline" status
    def DistributeCam(self) -> CameraModuleEnum:
        for key, value in CAM_STAT_DICT.items():
            if value == "Offline":
                return key
        return None
    
    #Toggle camera status
    def ToggleCamStatus(self, cams: CameraModuleEnum) -> None:
        if CAM_STAT_DICT[cams] == "Offline":
            CAM_STAT_DICT[cams] = "Online"
        else:
            CAM_STAT_DICT[cams] = "Offline"

    #Get camera footage
    def GetCamFootage(self, source: str) -> any:
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
    
    #Get camera IP
    def ReadIP(file_path):
        try:
            with open(file_path, 'r') as file:
                # Read the content of the file
                content = file.readline().strip()
                
                # Extract the IP address from the content
                if content.startswith("IP:"):
                    ip_address = content.split(" ")[1]
                    return ip_address
                else:
                    raise ValueError("Invalid file format. Expected 'IP: <url>'.")
        except FileNotFoundError:
            return "The file does not exist."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    #Change camera IP
    def ChangeIP(file_path, new_ip):
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
            else:
                raise ValueError("Invalid file format. Expected 'IP: <url>'.")
        except FileNotFoundError:
            return "The file does not exist."
        except Exception as e:
            return f"An error occurred: {str(e)}"