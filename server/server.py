# Variables naming convention
# - GLOBAL_VARIABLE 
# - class_variable_
# - ClassName
# - variable_name
# - k_constant_variable
# - FunctionName

from flask import Flask, jsonify
from flask_lib import Get, APP, WebhookSend, Post
from os import getenv
from dotenv import load_dotenv
from opencvtest import capture_photos

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

@Post
async def Capture() -> str:
    success: bool = capture_photos()
    if success:
        return jsonify({"message": "Photos captured successfully!"}), 200
    else:
        return jsonify({"message": "Failed to capture photos."}), 500


def flask_run():
    APP.run( host=HOST_IP, port=HOST_PORT)
    
@post
def main():
    flask_run()
    
if __name__ == "__main__":
    main()
    