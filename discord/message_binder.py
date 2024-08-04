from discord import Message, Colour
from discord_message_lib import DiscordMessage
from responses_lib import RestfulClient, ApiServiceEnum, API_SERVICE_DICT


def get_response(message : Message, content: str, restful_client : RestfulClient) -> DiscordMessage:
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
    else:
        discord_message.SetMessage('I am not sure what you are asking for')
        
    return discord_message

def ServerStatus(*, context : DiscordMessage, restful_client : RestfulClient) -> None:
    context.CreateEmbed(title="Server API Service", description="Press the link to open server application", colour=Colour.red())
    
    for api in ApiServiceEnum:
        if API_SERVICE_DICT[api][0]:
            context.EmbedAddField(name=API_SERVICE_DICT[api][1], value=restful_client.CreateUrl(restful_client.service_dict_[api.value]), inline=False)
    
def CamsStatus(*, context : DiscordMessage, restful_client : RestfulClient) -> None:
    context.CreateEmbed(title="Cams Status", description="Press the link to open cams application", colour=Colour.green())
    
    '''
    for cams in <cams_dict>:
        context.EmbedAddField(name=<cams_name> + <status>, value=restful_client.CreateUrl(restful_client.service_dict_[api.value]), inline=False)
    '''
    