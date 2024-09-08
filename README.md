# Impostor Detection System 
This is a client-server application for the intruder detection system using an edge computer.<br />
Each application can be run independently as a node and each node can be responsible for one role.<br />
Currently there is no implementation for multiple node server application as this project is just to test the effectiveness of edge computing intruder detection system.

# Architecture
![General Architecture](https://github.com/user-attachments/assets/006722bf-1ec1-4d0b-99ea-407b94b87709)
<br />The main architecture is split into 2 sections.<br />
1. Server (our server, 3rd party discord server)
2. Client (camera module and discord bot)

## Special note
These files are shared across each application
1. Camera_lib.py
2. respnses_lib.py
3. flask_lib.py

## System Overview
![Actiivity Diagram](https://github.com/user-attachments/assets/110a68ab-21c7-4258-9080-e9f96da8653b)
<br/>This is the flow of the system

## Server
![Server Module](https://github.com/user-attachments/assets/def03fa0-fa10-4123-ab30-522eb969acc5)
The server is responsible for<br />
1. Database (The database currently is stored in a file system and no actual storage is added)
2. API, the server provides services for the client
3. Human Recognition module (register friendlies)
4. Webhook to send notifications in the discord application
   
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
1. Camera Module (connection with camera via HTTP)
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
2. (keyword) help<br />
![help command list](https://github.com/user-attachments/assets/82a73817-aacb-4d43-9849-06fe4929a7fe)


# Version
1.0.0

# Dependencies
## server.py dependencies
| Package            | Version    |
|--------------------|------------|
| aiohttp            | 3.10.5     |
| deepface           | 0.0.93     |
| discord            | 2.3.2      |
| Flask              | 3.0.3      |
| opencv-python      | 4.10.0.84  |
| python-dotenv      | 1.0.1      |
| tf_keras           | 2.17.0     |

## client.py dependencies
| Package Name     | Version    |
|------------------|------------|
| opencv-python    | 4.10.0.84  |
| python-dotenv    | 1.0.1      |
| requests         | 2.32.3     |
| ultralytics      | 8.2.75     |
| tensorflow       | 2.17.0     |
| torch            | 2.2.0      |
| torchvision      | 0.17.0     |

## register_face.py dependencies
| Package Name     | Version    |
|------------------|------------|
| opencv-python    | 4.10.0.84  |
| python-dotenv    | 1.0.1      |
| requests         | 2.32.3     |

## discord/app.py dependencies
| Package Name     | Version    |
|------------------|------------|
| python-dotenv    | 1.0.1      |
| discord          | 2.3.2      |
| requests         | 2.32.3     |

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
This class is the object for the camera object. The key is the object and the value is the location of the camera

2. CameraObject / SelfCameraObject<br />
![image](https://github.com/user-attachments/assets/c0dda11e-8365-4e94-9b9a-02ed6405e91f)<br />
Camera Object is used for the status of the server<br />
Self Camera Object is used for clients for self-naming purposes

### flask_lib.py
This file acts as an adapter for ease of use of the flask library.<br />
This file contains decorator factory and webhook templates. <br />
This file also has a default function ApiService() to create a default service. <br /> 
<br />
1. CallbackFunctioRoute <br />
![image](https://github.com/user-attachments/assets/fa6c54e5-ff10-477b-8de2-bfa9445e18ae) <br />
This keeps track of what function the software needs to register for the flask route. <br />
The key is the name of the function (Case Sensitive, function name === variable name) <br />
The value is the route the server wants to host the function

2. CALLBACK_FUNCTION_ROUTE <br />
![image](https://github.com/user-attachments/assets/b38b4ba5-0a5a-444f-b474-203bfef28418) <br />
This function is used to convert enum to dictionary.<br />
It acts as a static variable

3. Decorator<br />
This is a method to generate a function using the flask format.<br />
During the runtime, the server will first read through all the services and call the decorator to generate each function and its route automatically. <br />
   a. @Callback is for a generic service<br />
   b. @Get : get method<br />
   c. @Post : post method<br />
   d. @GetPost : get and post method<br />
   e. Other method can be added if needed<br />
   ![image](https://github.com/user-attachments/assets/62613a33-3e83-404a-b31e-be3784dde2b7)

5. Webhook<br />
This function is used to send webhooks.

### responses_lib
This file acts as an adapter for ease of use of the requests library.<br />
<br />
1. ApiServiceEnum<br />
![image](https://github.com/user-attachments/assets/5df778ea-6855-4fd1-be99-1cb85d82093f)<br />
This class is a link to the server service API.<br />
It key is the object and the value is for the keyword for the dictionary in the server.

2. API_SERVICE_DICT<br />
![image](https://github.com/user-attachments/assets/59995d4e-0e85-48b6-a24e-078a088070a2)<br />
This dictionary is used for the discord application or other UI to display visible API for users and hide some developer functions for functions used only

3. UpdateServiceDict<br />
![image](https://github.com/user-attachments/assets/2bef1899-8db0-475f-b1a3-5ab5770ef416)<br />
This function is used to obtain API service from the server.<br />
This function may fail if the client could not access the server. 

## Discord bot
### message_binder.py
1. BotFeatureEnum (class) <br />
![image](https://github.com/user-attachments/assets/64df3dc4-a862-49da-8304-7e838af0e413) <br />
This class is the object for each response.<br />
The key is the object and the value is the keyword the bot responds to <br />
Unknown is a wildcard that is only used for exceptions on the keyword

2. UMAPENUMFUNC <br />
![image](https://github.com/user-attachments/assets/eed235fc-100a-4ec3-b23d-75e3fe0938c3) <br />
This variable registers the function for each response using a dictionary<br />
It acts as a static variable

3. UMAPBOTFEATUREDESCRIPTION <br />
![image](https://github.com/user-attachments/assets/3507b66a-b155-408f-b737-f3a84f3abe96) <br />
This variable is responsible for showing the user the description on each keyword for the help_ function <br />
It acts as a static variable

4. UMAPBOTFEATURE <br />
![image](https://github.com/user-attachments/assets/460f45ee-4ed6-43c5-94da-6bd22357594a) <br />
This variable is to convert text read from discord back to enum<br />
It acts as a static variable


