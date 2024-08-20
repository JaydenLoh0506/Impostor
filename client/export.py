#this file is to generate lite model of YOLO model
#Both full YOLO model and generated lite model will be
#in the same directory as this file

#Date : 20/8/2024
#Software Version : 0.0.1

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Export the model to TFLite format
model.export(format="tflite")  # creates 'yolov8n_float32.tflite'

# Load the exported TFLite model
tflite_model = YOLO("yolov8n_float32.tflite")