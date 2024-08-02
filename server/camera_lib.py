from enum import Enum, unique

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