from discord import Message, Colour
from discord_message_lib import DiscordMessage
from responses_lib import RestfulClient, ApiServiceEnum, API_SERVICE_DICT
from camera_lib import CameraModule, CameraModuleEnum, CameraObject
from typing import Callable

# Unordered Map
UMAPCAMS : dict[str, CameraModuleEnum] = {}
for cam in CameraModuleEnum:
    UMAPCAMS[cam.name] = cam
    
class BotObject:
    def __init__(self, *, message : Message, content : str, restful_client : RestfulClient, camera_module : CameraModule) -> None:
        self.message_ : Message = message
        self.content_ : str = content
        self.restful_client_ : RestfulClient = restful_client
        self.camera_module_ : CameraModule = camera_module
        self.discord_message_ : DiscordMessage = DiscordMessage()

def GetResponse(bot_object : BotObject) -> DiscordMessage:
#def get_response(message : Message, content: str) -> DiscordMessage:
    """ 
    This is the generic function for binder.
    It will be the place that store all endpoint for the discord bot

    :param message: Context for the Message
    :type message: Message
    :param content: Message from the discord user input
    :type content: str
    :return: Return the DiscordMessage object
    :rtype: DiscordMessage
    """
    word = bot_object.content_.split(' ')[0].lower()
    if word in UMAPFEATURE:
        RunFunction(func=UMAPFEATURE[word], bot_object=bot_object)
    else:
        RunFunction(func=UMAPFEATURE['unknown'], bot_object=bot_object)
    return bot_object.discord_message_

# message function for dict
def BotStatus(bot_object : BotObject) -> None:
    if 'Success' == bot_object.restful_client_.GetText(bot_object.restful_client_.CreateUrl(route=bot_object.restful_client_.service_dict_[ApiServiceEnum.TestComms.value])):
        bot_object.discord_message_.SetMessage('Communication is successful')
    else:
        bot_object.discord_message_.SetMessage('Communication failed')
        
def BotApi(bot_object : BotObject) -> None:
    ServerStatus(context=bot_object.discord_message_, restful_client=bot_object.restful_client_)
    
def BotCams(bot_object : BotObject) -> None:
    CamsStatus(context=bot_object.discord_message_, restful_client=bot_object.restful_client_, camera_module=bot_object.camera_module_)
    bot_object.discord_message_.SetMessage('Cams Status')
    
def BotUnknown(bot_object : BotObject) -> None:
    bot_object.discord_message_.SetMessage('I am not sure what you are asking for')
        
# Unordered Map
UMAPFEATURE : dict[str, Callable[[BotObject], None]] = {
    'status' : BotStatus,
    'api' : BotApi,
    'cams' : BotCams,
    'unknown' : BotUnknown
}

# funciton
def RunFunction(*,func : Callable[[BotObject], None], bot_object : BotObject) -> None:
    func(bot_object)

def ServerStatus(*, context : DiscordMessage, restful_client : RestfulClient) -> None:
    context.CreateEmbed(title="Server API Service", description="Press the link to open server application", colour=Colour.red())
    
    for api in ApiServiceEnum:
        if API_SERVICE_DICT[api][0]:
            context.EmbedAddField(name=API_SERVICE_DICT[api][1], value=restful_client.CreateUrl(restful_client.service_dict_[api.value]), inline=False)
    
def CamsStatus(*, context : DiscordMessage, restful_client : RestfulClient, camera_module : CameraModule) -> None:
    context.CreateEmbed(title="Cams Status", description="Press the link to open cams application", colour=Colour.green())
    
    CamsDictUpdate(camera_module=camera_module, restful_client=restful_client)
    
    for cam_obj in camera_module.cam_dict_.values():
        if cam_obj.status_ == 'Offline':
            context.EmbedAddField(name=f"{cam_obj.name_}", value='Offline', inline=False)
        else:
            context.EmbedAddField(name=f"{cam_obj.name_}({cam_obj.location_})", value=restful_client.CreateUrl(f'{restful_client.service_dict_[ApiServiceEnum.Image.name]}{cam_obj.name_}'), inline=False)

    
def CamsDictUpdate(*, camera_module : CameraModule, restful_client : RestfulClient) -> None:
    temp : dict[str, dict[str, str]] = restful_client.GetJson(restful_client.CreateUrl(restful_client.service_dict_[ApiServiceEnum.CamDict.value])) # type: ignore
    for key, value in temp.items():
        camera_module.cam_dict_[UMAPCAMS[key]] = CameraObject(name=value['name'], location=value['location'], status=value['status'])
        
        
        