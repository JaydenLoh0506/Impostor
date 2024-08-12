# camtest.py

from deepface import DeepFace
import cv2
import os
import time

# Path settings
DB_PATH = "image"
MODEL_NAME = 'Facenet'  # Consider using a smaller model for faster processing

def recognize_faces(image_path):
    try:
        # Read the image
        frame = cv2.imread(image_path)
        if frame is None:
            return {"error": "Failed to read image"}

        # Detect faces using OpenCV
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        results = []

        for (x, y, w, h) in faces:
            # Extract the face region
            face_img = frame[y:y+h, x:x+w]
            TEMP_IMAGE_PATH = 'temp_face.png'
            cv2.imwrite(TEMP_IMAGE_PATH, face_img)

            try:
                # Measure latency for face recognition using DeepFace
                start_time = time.time()
                find_results = DeepFace.find(img_path=TEMP_IMAGE_PATH, db_path=DB_PATH, model_name=MODEL_NAME, enforce_detection=False)
                end_time = time.time()
                deepface_latency = end_time - start_time

                # Extract folder names from the results
                if find_results and not find_results[0].empty:
                    folder_name = find_results[0]['identity'].apply(lambda x: os.path.basename(os.path.dirname(x))).iloc[0]
                else:
                    folder_name = "Intruder"

                results.append({
                    "face_position": (x, y, w, h),
                    "name": folder_name,
                    "latency": deepface_latency
                })

            except ValueError as ve:
                results.append({
                    "face_position": (x, y, w, h),
                    "error": str(ve)
                })

            finally:
                # Clean up the temporary image file
                if os.path.exists(TEMP_IMAGE_PATH):
                    os.remove(TEMP_IMAGE_PATH)

        return {"results": results}

    except Exception as e:
        return {"error": str(e)}
