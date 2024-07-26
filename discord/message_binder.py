from discord import Message, Colour
from discord_message_lib import DiscordMessage
from responses_lib import RestfulClient, ApiServiceEnum, API_SERVICE_DICT


#def get_response(message : Message, content: str, restful_client : RestfulClient) -> DiscordMessage:
def get_response(message : Message, content: str) -> DiscordMessage:
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
        discord_message.SetMessage('I am alive')
    elif word[0].lower() == 'web':
        #discord_message.SetMessage(restful_client.CreateUrl(restful_client.service_dict_[ApiServiceEnum.Index.value]))
        discord_message.SetMessage('Oh')
        discord_message.CreateEmbed(title="Webhook", description="This is a webhook", colour=Colour.green())
        discord_message.EmbedAddField(name="Field 1", value="Value 1", inline=False)
    else:
        discord_message.SetMessage('I am not sure what you are asking for')
        
    return discord_message

def ServerStatus(*, context : DiscordMessage, restful_client : RestfulClient) -> None:
    context.CreateEmbed(title="Server API Service", description="Press the link to open server application", colour=Colour.red())
    
    for api in ApiServiceEnum:
        context.EmbedAddField(name=API_SERVICE_DICT[api], value=restful_client.CreateUrl(restful_client.service_dict_[api.value]), inline=False)
    
def CamsStatus(*, context : DiscordMessage, restful_client : RestfulClient) -> None:
    context.CreateEmbed(title="Cams Status", description="Press the link to open cams application", colour=Colour.green())
    
    '''
    for cams in <cams_dict>:
        context.EmbedAddField(name=<cams_name> + <status>, value=restful_client.CreateUrl(restful_client.service_dict_[api.value]), inline=False)
    '''
    