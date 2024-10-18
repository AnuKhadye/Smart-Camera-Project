# Written by Fernando Campos on 29/03/2024

import serial  # Library for serial communication
import cv2  # Library for computer vision
import paho.mqtt.client as paho
from inference_sdk import InferenceHTTPClient
import time  # Import the time module

# Define serial port and baud rate (match Arduino settings)
ser = serial.Serial('COM5', 9600) # Port where Aduino Board is connected  

# Roboflow Model details 
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="gCKCuAfD1ZqFgdPTYvLS")
model_id = "coco/9"  

def capture_and_process_image():
    """Captures an image from webcam, performs basic processing, and sends for object detection."""
    # Capture image from webcam
    cap = cv2.VideoCapture(0)

    # Check if webcam opened successfully
    if not cap.isOpened():
        print("Error opening webcam")
        return

    # Capture frame-by-frame
    
    ret, frame = cap.read()

    # Check if frame was captured successfully
    if not ret:
        print("Error capturing frame")
        cap.release()
        return

    # Save captured image
    cv2.imwrite('picture.jpg', frame)

    # Perform object detection using Roboflow model
    detections = CLIENT.infer("picture.jpg", model_id=model_id)
    result = return_predictions(detections)
    print("Object detection results:")
    print(result)

    # Release the capture
    cap.release()


def return_predictions(result):
    number_of_predictions = len(result["predictions"])
    prediction_list = []
    for number in range(0, number_of_predictions):
        prediction_list.append(result["predictions"][number]["class"])
        print(result["predictions"][number]["class"])
    return prediction_list


def mqtt_publish(ip="192.168.1.157", port=1883):
    file = open("picture.jpg", "rb")
    payload = file.read()
    client = paho.Client(paho.CallbackAPIVersion1, "Fernando_Campos")
    client.connect(ip, port)
    client.publish("obj-rec", payload)
    client.disconnect()

def simulate_trigger():
    # Simulate trigger message (for testing)
    trigger_message = "Trigger: Capture image"

    if trigger_message == "Trigger: Capture image":
        # Capture and process image
        capture_and_process_image()
        # Additional processing after image capture (optional)

def main():
        
    # Flag to indicate trigger simulation
    trigger_simulated = False

    while True:
        
        # Simulate trigger (if not already done)
        if not trigger_simulated:
            simulate_trigger()
            trigger_simulated = True
    
        # Check for serial trigger from Arduino
        if ser.inWaiting() > 0:
            trigger_message = ser.readline().decode('utf-8').rstrip()
            if trigger_message == "Trigger: Capture image":
                print("Trigger received from Arduino, capturing image!")
                capture_and_process_image()
                mqtt_publish()  # If using MQTT for image transmission
            else:
                print("Unknown message received:", trigger_message)
        else:
            print("Waiting for trigger...")
        time.sleep(1)  # Adjust delay between checks 

if __name__ == "__main__":
    main()
