# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from flask_lib import Get, APP, WebhookSend
from os import getenv
from dotenv import load_dotenv

# load the environment variables
load_dotenv()
WEBHOOK_URL : str = str(getenv('DISCORD_WEBHOOK'))
#WEBHOOK_URL_TEST : str = str(getenv('DISCORD_WEBHOOK_TEST'))
HOST_IP : str = str(getenv('SERVER_IP'))
HOST_PORT : int = int(str(getenv('SERVER_PORT')))

# Centralised computing
@Get
async def Index():
    await WebhookSend(webhook_url=WEBHOOK_URL, content="Index Page")
    return f"Message Sent"

@Get
async def Test2() -> str:
    return "Hell2o 2World"

def flask_run():
    APP.run( host=HOST_IP, port=HOST_PORT)
    
    
def main():
    flask_run()
    
if __name__ == "__main__":
    main()
    