# opencvtest.py
import cv2
import os
import numpy as np
import random
from dotenv import load_dotenv
from responses_lib import RestfulClient, ApiServiceEnum
from os import getenv
from camera_lib import CameraModule, CameraModuleEnum
from sys import exit

load_dotenv()
RESTFULCLIENT : RestfulClient = RestfulClient(str(getenv('SERVER_IP')), int(str(getenv('SERVER_PORT'))))  
CAMERA_MODULE : CameraModule = CameraModule()
CONFIG_PATH: str = "config.txt"

#Check server status
def ServerStatus() -> None:
    try:
        if not RESTFULCLIENT.server_api_:
            RESTFULCLIENT.UpdateServiceDict()
            RESTFULCLIENT.server_api_ = True
    except Exception as e:
        #print(e)
        exit("Server is offline")

def adjust_brightness(image: np.ndarray, value: int) -> np.ndarray:
    """
    Adjust the brightness of the image by a specified value.
    """
    hsv: np.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v = np.clip(v, 0, 255)
    final_hsv: np.ndarray = cv2.merge((h, s, v))
    image_bright: np.ndarray = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return image_bright

def add_instruction(image: np.ndarray, text: str, position: tuple[int, int]) -> np.ndarray:
    """
    Add an instruction text to the image at the specified position.
    """
    font: int = cv2.FONT_HERSHEY_SIMPLEX
    font_scale: float = 1.0
    font_color: tuple[int, int, int] = (255, 255, 255)
    thickness: int = 2
    line_type: int = cv2.LINE_AA

    text_size: tuple[int, int] = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x: int = position[0]
    text_y: int = position[1] + text_size[1]

    cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, thickness, line_type)
    return image

def capture_photos() -> bool:
    """
    Capture 9 photos and save them with different brightness levels and instructions.
    """
    base_path: str = "image"
    
    source: str = ""
    if CAMERA_MODULE.read_config(CONFIG_PATH):
        source = CAMERA_MODULE.cam_.ip_
    else:
        exit("Please turn on your camera")

    cap: cv2.VideoCapture = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    photo_count: int = 0
    photos: list[np.ndarray] = []

    print("Press 'u' to capture a photo. Capture 9 photos.")

    while photo_count < 9:
        ret: bool
        frame: np.ndarray
        ret, frame = cap.read()

        cv2.imshow('frame', frame)

        key: int = cv2.waitKey(1) & 0xFF
        
        if key == ord('u'):
            photos.append(frame)
            photo_count += 1
            print(f"Captured photo {photo_count}")

    cap.release()
    cv2.destroyAllWindows()

    name: str = input("Enter your name: ")

    user_dir: str = base_path + "/" + name
    #user_dir: str = os.path.join(base_path, name)
    #os.makedirs(user_dir, exist_ok=True)

    brightness_values: list[int] = [-50, 0, 50]

    positions: list[tuple[int, int]] = [
        (10, 10),
        (frame.shape[1] - 100, 10),
        (10, frame.shape[0] - 100),
        (frame.shape[1] - 100, frame.shape[0] - 100)
    ]

    instructions: list[str] = ["Left", "Top", "Right", "Down"]

    for i in range(4):
        photos[i] = add_instruction(photos[i], instructions[i], positions[i])

    random_instructions: list[str] = ["Instruction 1", "Instruction 2", "Instruction 3", "Instruction 4", "Instruction 5"]
    for i in range(4, 9):
        random_position: tuple[int, int] = (random.randint(10, photos[i].shape[1] - 100), random.randint(10, photos[i].shape[0] - 100))
        random_text: str = random.choice(random_instructions)
        photos[i] = add_instruction(photos[i], random_text, random_position)
        random_instructions.remove(random_text)

    for i, photo in enumerate(photos):
        for j, brightness in enumerate(brightness_values):
            adjusted_photo: np.ndarray = adjust_brightness(photo, brightness)
            ret, adjusted_photo = cv2.imencode(".jpg", adjusted_photo)
            adjusted_photo = adjusted_photo.tobytes()
            new_path: str = user_dir + "/" + f"photo_{i + 1}_brightness_{j + 1}.jpg"
            #new_path: str = os.path.join(user_dir, f"photo_{i + 1}_brightness_{j + 1}.jpg")
            # cv2.imwrite(new_path, adjusted_photo)
            print(f"Saved {new_path}")
            url : str = RESTFULCLIENT.CreateUrl(RESTFULCLIENT.service_dict_ [ApiServiceEnum.FaceRecognition.value])
            response : str = RESTFULCLIENT.PostFile(url, new_path, adjusted_photo)
            print(response)
    return True

if __name__ == "__main__":
    ServerStatus()
    capture_photos()