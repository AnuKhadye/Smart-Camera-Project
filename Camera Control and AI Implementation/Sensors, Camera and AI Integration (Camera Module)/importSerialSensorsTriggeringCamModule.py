# Written by Fernando Campos on 26/03/2024

import serial  # Library for serial communication
import cv2  # Library for computer vision
from inference_sdk import InferenceHTTPClient
import base64  # Library for base64 encoding/decoding
import os  # Library for file system operations

# Define serial port and baud rate (match Arduino settings)
ser = serial.Serial('COM5', 9600)  # Port where Arduino Board is connected

# Roboflow Model details (replace with your API key and model ID)
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="YOUR_API_KEY")
model_id = "coco/9"  # Replace with your Roboflow model ID


def receive_image_data():
    """Receives a base64 encoded image string from the serial port."""
    data = ""
    while True:
        incoming = ser.readline().decode('utf-8').strip()
        if incoming.startswith("Sending image (base64 encoded): "):
            # Extract base64 encoded image data
            data = incoming[32:]  # Remove prefix
            break
    return data


def decode_and_save_image(encoded_data):
    """Decodes the base64 encoded image data and saves it as a temporary file."""
    # Decode base64 data
    decoded_data = base64.b64decode(encoded_data)

    # Save the decoded data as a temporary image file
    with open("received_image.jpg", "wb") as f:
        f.write(decoded_data)


def capture_and_process_image():
    """Processes the received and decoded image for object detection."""

    # Use the received_image.jpg instead of webcam capture
    frame = cv2.imread("received_image.jpg")

    # Check if image was read successfully
    if frame is None:
        print("Error reading received image")
        return

    # ... rest of your object detection logic using OpenCV and Roboflow ...

    # Delete the temporary image after processing
    os.remove("received_image.jpg")


def return_predictions(result):
    number_of_predictions = len(result["predictions"])
    list = []
    for number in range(0, number_of_predictions):
        list.append(result["predictions"][number]["class"])
        print(result["predictions"][number]["class"])
    return list


def main():
    while True:
        data = ser.readline().decode('utf-8').strip()  # Read data from Arduino
        if data == "trigger_camera":
            print("Trigger received from Arduino!")

            # Receive and decode the image data
            encoded_data = receive_image_data()
            decode_and_save_image(encoded_data)

            # Process the received image
            capture_and_process_image()
        else:
            print(f"Received data: {data}")  # Print any other received data for debugging


if __name__ == "__main__":
    main()
