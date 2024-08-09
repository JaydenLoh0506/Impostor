from os import getenv
from dotenv import load_dotenv
from discord import Client, Intents, Message
from discord_message_lib import DiscordMessage
from message_binder import get_response
from responses_lib import RestfulClient
from camera_lib import CameraModule

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
INTENTS : Intents = Intents.default()
INTENTS.message_content = True
CLIENT : Client = Client(intents=INTENTS)

CAMERAMODULE : CameraModule = CameraModule()
RESTFULCLIENT : RestfulClient = RestfulClient(str(getenv('SERVER_IP')), int(str(getenv('SERVER_PORT'))))
    
# Send Message
async def SendMessage(message: Message, content: str) -> None:
    if not content:
        await message.channel.send("You didn't provide any message content.")
        return
    
    try:
        if not RESTFULCLIENT.server_api_:
            RESTFULCLIENT.UpdateServiceDict()
            RESTFULCLIENT.server_api_ = True
        response : DiscordMessage = get_response(message, content, RESTFULCLIENT, CAMERAMODULE)
        await message.channel.send(content=response.message_, embed=response.embed_) # type: ignore
    except Exception as e:
        print(e) # WHO CARES ABOUT EXCEPTIONS
        await message.channel.send("Server is offline")
        

# Event Handlers
@CLIENT.event
async def on_ready() -> None:
    print(f'{CLIENT.user} has connected to Discord!')
    
@CLIENT.event
async def on_message(message: Message) -> None:
    if message.author == CLIENT.user:
        return
    
    if message.content.startswith('im'):
        await SendMessage(message, message.content[3:])

def bot_run() -> None:
    CLIENT.run(token=TOKEN) # type: ignore
    
if __name__ == '__main__':
    bot_run()