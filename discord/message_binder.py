from discord import Message, Colour
from discord_message_lib import DiscordMessage
from responses_lib import RestfulClient, ApiServiceEnum, API_SERVICE_DICT
from camera_lib import CameraModule, CameraModuleEnum, CameraObject

# Unordered Map
UMAPCAMS : dict[str, CameraModuleEnum] = {}
for cam in CameraModuleEnum:
    UMAPCAMS[cam.name] = cam

def get_response(message : Message, content: str, restful_client : RestfulClient, camera_module : CameraModule) -> DiscordMessage:
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
    discord_message : DiscordMessage = DiscordMessage()
    word = content.split(' ')
    if word[0].lower() == 'status':
        if 'Success' == restful_client.GetText(restful_client.CreateUrl(route=restful_client.service_dict_[ApiServiceEnum.TestComms.value])):
            discord_message.SetMessage('Communication is successful')
        else:
            discord_message.SetMessage('Communication failed')
    elif word[0].lower() == 'api':
        ServerStatus(context=discord_message, restful_client=restful_client)
    elif word[0].lower() == 'cams':
        CamsStatus(context=discord_message, restful_client=restful_client, camera_module=camera_module)
        discord_message.SetMessage('Cams Status')
    else:
        discord_message.SetMessage('I am not sure what you are asking for')
        
    return discord_message

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