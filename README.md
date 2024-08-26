# Impostor
This is a client server application for the intruder detection system using edge computer

# Architecture
![General Architecture](https://github.com/user-attachments/assets/006722bf-1ec1-4d0b-99ea-407b94b87709)
<br />The main architecture is split into 2 section.<br />
1. Server (our own server, 3 rd part discord server)
2. Client (camera module and discord bot)

## Special note
These files are shared across each application
1. Camera_lib.py
2. respnses_lib.py
3. flask_lib.py

## Server
![Server Module](https://github.com/user-attachments/assets/def03fa0-fa10-4123-ab30-522eb969acc5)
The server is responsible for<br />
1. Database (Database currently is storing in file system and no actual storage is added)
2. API, the server provides services for the client
3. Human Recognition module (register friendlies)
4. Webhook to sent notification in discord application
   
## Run Server 
1. Install dependencies (notes* pip install flask[async])
2. Provide the .env file with the following key<br />
    a. DISCORD_WEBHOOK=(your token here)<br />
    b. SERVER_IP=(your server IP)<br />
    c. SERVER_PORT=(your server port)
3. Run server.py


## Client
![image](https://github.com/user-attachments/assets/4296b08b-afb1-4f5b-ad9b-902fcdfe757e)<br />
The client is responsible for<br />
1. Camera Module (connection with cameara via https)
2. Yolo (preprocessing for intruder detection)
3. API (communication with the server)
4. Add character for face recognition

## Run client
1. Install dependencies
2. Provide the .env file with the following<br />
    a. SERVER_IP=(your server IP)<br />
    b. SERVER_PORT=(your server port)
3. Provide the IP for the camera and its location
4. Run client.py

## Torch Export to Lite model
1. change the location on the full model in export.py
2. Run export.py 

## Discord bot
![image](https://github.com/user-attachments/assets/d1c55374-d79b-4f5f-a154-01eeac662611)<br />
Discord bot is responsible for<br />
1. Provide help for users in discord message
2. Get the status of the system from the server

## Run bot
1. Install dependencies
2. Create a discord bot application [here](https://discord.com/developers/applications)
3. Provide the .env file with the following<br />
    a. SERVER_IP=(your server IP)<br />
    b. SERVER_PORT=(your server port)<br />
    c. DISCORD_TOKEN=([get you token in your application](https://discordpy.readthedocs.io/en/stable/discord.html))
4. Run app.py

## Call the bot
1. Keyword bot in app.py
2. (keyword) help

# Version
1.0.0

# Dependencies
TBA

# Variable naming convention
1. ClassName
2. variable_name
3. class_variable_
4. GLOBALVARIABLE
5. k_constant_variable
6. FunctionName

# Software Expansion
## Library
### camera_lib.py
1. CameraModuleEnum<br />
![image](https://github.com/user-attachments/assets/8d673c33-91d1-4d25-8e61-7aae3c542cbf)<br />
This class is the object for the camera object. The key is object and the value is the location for the camera


## Discord bot
### message_binder.py
1. BotFeatureEnum (class) <br />
![image](https://github.com/user-attachments/assets/64df3dc4-a862-49da-8304-7e838af0e413) <br />
This class is the object for each responses. The key is the object and the value is the keyword the bot response too<br />
Unknown is a wildcard that only use for exception on the keyword

2. UMAPENUMFUNC <br />
![image](https://github.com/user-attachments/assets/eed235fc-100a-4ec3-b23d-75e3fe0938c3) <br />
This variable is register the function for each responses using a dictionary<br />
It act as a static variable

3. UMAPBOTFEATUREDESCRIPTION <br />
![image](https://github.com/user-attachments/assets/3507b66a-b155-408f-b737-f3a84f3abe96) <br />
This variable is responsible to show the user the description on each keyword for help_ function <br />
It act as a static variable

4. UMAPBOTFEATURE <br />
![image](https://github.com/user-attachments/assets/460f45ee-4ed6-43c5-94da-6bd22357594a) <br />
This variable is to convert text read from discord back to enum<br />
It act as a static variable


