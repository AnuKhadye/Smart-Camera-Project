# Written by Fernando Campos

import serial  # Library for serial communication
import cv2  # Library for computer vision
import paho.mqtt.client as paho
from inference_sdk import InferenceHTTPClient
import time  # Import the time module
import datetime
import time
import os
import paho.mqtt.client as mqtt
from paho.mqtt import client as mqtt_client
from inference_sdk import InferenceHTTPClient
import sqlite3
import bcrypt
import re  # For regular expressions

# To let us know when message is published
def on_publish(client, userdata, result):
  print("Message published")
#Setting up the broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Test")
client.on_publish = on_publish
client.username_pw_set("your_username", "your_password")
client.connect("broker.mqtt.cool", 1883)


# function to predict object (written by Semen)
def get_predictions(photopath, client):
    apiUrl = "https://detect.roboflow.com"
    apiKey = "gCKCuAfD1ZqFgdPTYvLS"
    modelId = "coco/9"
    topic = "cam174"
    inference_client = InferenceHTTPClient(api_url=apiUrl, api_key=apiKey)
    detections = inference_client.infer(photopath, model_id=modelId)
    print("Detections:", detections)    
    result = return_predictions(detections)   
    payload = "Predictions: " + ', '.join(result)
    client.publish(topic, payload)
    print("Predictions sent to the broker")
    return result

 # function to predict flowers
def get_flower_predictions(photopath):
  CLIENT = InferenceHTTPClient(api_url="https://detect.roboflow.com",api_key="QMmHe6zUMt?key=YzYb205ePU")
  detections = CLIENT.infer(photopath,model_id="EfficientNetB2")
  print(detections)
  result = return_flower_predictions(detections)
  payload = "Flower Predictions: " + ', '.join(result)
  client.publish("cam174/FLpredictions", payload)
  print("Flower Predictions sent to broker")
  return result




# function to make a list of reasult 
def return_predictions(dictionary):
  number_of_predictions = len(dictionary["predictions"])
  result_list = []
  for number in range(number_of_predictions):
    result_list.append(dictionary["predictions"][number]["class"])
  print(result_list)
  return result_list



# function to return flower prediction
def return_flower_predictions(dictionary):
  number_of_predictions = len(dictionary["predictions"])
  result_list = []
  for number in range(number_of_predictions):
    result_list.append(dictionary["predictions"][number]["class"])
  print(result_list)
  return result_list

#Function to take the pic
def snap_and_predict():
  cam = cv2.VideoCapture(0)
  result, image = cam.read()
  if result:
    cv2.imwrite('picture.jpg', image)
    predictions = get_predictions("picture.jpg")

    showpic(image)
    os.remove("picture.jpg")
    cam.release()
  else:
    print("no picture")
 flower_predictions = get_flower_predictions("picture.jpg")


if __name__ == "__main__":
  
  
# Topic-1  Publishing image processing completion status to "image_processing_completed" topic
image_processing_completed_topic = "ip174"
image_processing_completed_message = "Image processing completed"
client.publish(image_processing_completed_topic, image_processing_completed_message)

# Topic-2 Publishing object detection results to "ODR174" topic
object_detection_results_topic = "cam174"
object_detection_results_message = "Object detection results: " + ', '.join(predictions)
client.publish(object_detection_results_topic, object_detection_results_message)


  
  '''topic2 = "time174"  #topic for time
  message2 = time.strftime('%Y-%m-%d %H:%M:%S')
  client.publish(topic2, message2)
  
  greeting topic
  hour = int(time.strftime('%H'))
  if 3 <= hour < 12:
      greeting = "Good Morning"
  elif 12 <= hour < 17:
      greeting = "Good Afternoon"
  elif 17 <= hour < 21:
      greeting = "Good Evening"
  else:
      greeting = "Good Night"
  topic3 = "gr174"
  message3 = greeting
  client.publish(topic3, message3)
  
  snap_and_predict()  #Run the function'''
  #For the topics and the format of the time, I've made them into a variable strings
Time_Layout = '%Y-%m-%d %H:%M:%S'
Topic_For_Time = "Time_MQTT"
Topic_For_Greeting = "gr174"


def for_current_time(client): #This function is defined to convert the time to a string and sends it to the MQTT Topic
    present_time = datetime.datetime.now().strftime(Time_Layout)
    client.publish(Topic_For_Time, present_time)
    print("The current published time: ", present_time)


def for_present_greetings(): #This function is defined to get the correct greeting based on the present time
    now = datetime.datetime.now() #This will get the time, using datetime.datetime with now variable
    hour = now.hour #This will get the hour, using now.hour with hour variable
    greetings_and_times_order = [ #This has tuples with appropriate time range and greeting for each one
       ("Good Morning!", range(3, 12)),
       ("Good Afternoon!", range(12, 17)),
       ("Good Evening!", range(17, 21)),
       ("Good Night!", tuple(range(21, 24)) + tuple(range(0, 3)))
   ]

    greeting = None
    for i, greeting_range in greetings_and_times_order: #The for function will check the range
        if hour in greeting_range: #This will check the current hour in the range
            greeting = i
            break
    return greeting #This will return the appropriate greeting

def connect_to_mqtt(): #This function is used to connect to the MQTT Broker
    def on_connect_mqtt(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to the MQTT Broker") #Message when it connect
            client.loop_start()
        else:
            print(f"Failed to connect with the MQTT Broker {rc}") #Message when it doesnt connect


    client = mqtt_client.Client()
    client.on_connect = on_connect_mqtt
    client.connect("broker.mqtt.cool", 1883) #The broker Address and port
    return client

def check_greeting_change(client): #This function does the check for new greetings and then publishes it
    while True:
        time.sleep(20) #This time sleep is to delay the loop to look for new greeting
        brand_new_greeting = for_present_greetings()
        if brand_new_greeting != client.greeting:
            client.greeting = brand_new_greeting
            client.publish(Topic_For_Greeting, brand_new_greeting)
            print("The new published greeting: ", brand_new_greeting) #This print the new greeting

if __name__ == "__main__": 
     # Written by Fernando Campos Staring Here 
    def validate_username(username):
      if len(username) < 6:
        raise ValueError("Username must be at least 6 characters long.")
      # You can add other username validation rules here (e.g., special characters)

    def validate_email(email):
      email_regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$"
      if not re.match(email_regex, email):
        raise ValueError("Invalid email address.")
      # You can add other email validation rules here (e.g., domain name checks)

    def register_user(username, email, password):
      # Connect to your database
      conn = sqlite3.connect('Users_Login_Images_Outcome.db')
      cursor = conn.cursor()

      try:
        # Check for empty fields
        if not username or not email or not password:
          raise ValueError("Username, email, and password cannot be empty.")

        # Validate username and email (optional, but recommended)
        validate_username(username)
        validate_email(email)

        # Check for duplicate username (assuming username is unique)
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
          raise ValueError("Username already exists. Please choose a different one.")

        # Hash password before storing (replace with a secure hashing algorithm like bcrypt)
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Insert new user into database with secure password
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()

        # Welcome message upon successful registration
        print("Welcome to the Maverick Smart Camera!")

        # Success message
        print("User registration successful!")

      except ValueError as e:
        print(f"Error: {e}")  # Informative error message

      finally:
        cursor.close()
        conn.close()

    def login_user(username, password):
      # Connect to your database
      conn = sqlite3.connect('Users_Login_Images_Outcome.db')
      cursor = conn.cursor()

      try:
        # Check for empty fields
        if not username or not password:
          raise ValueError("Username and password cannot be empty.")

        # Query for the user with the provided username
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
          raise ValueError("Invalid username or password.")

        # Hash the entered password and compare with stored hash
        entered_password_hash = bcrypt.hashpw(password.encode(), user[3])  # Assuming password_hash is at index 3

        if entered_password_hash != user[3]:  # Compare hashed passwords
          raise ValueError("Invalid username or password.")

        # Login successful message
        print(f"Welcome back, {user[1]}!")  # Assuming username is at index 1

      except ValueError as e:
        print(f"Error: {e}")  # Informative error message

      finally:
        cursor.close()
        conn.close() # By Fernando Campos finishes here.

    # Main execution block (initiate user interaction)
    if __name__ == '__main__':
      while True:
        print("Welcome! Please choose an option:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
          username = input("Enter username: ")
          email = input("Enter email: ")
          password = input("Enter password: ")
          register_user(username, email, password)
        elif choice == '2':
          username = input("Enter username: ")
          password = input("Enter password: ")
          login_user(username, password)
        elif choice == '3':
          print("Exiting...")
          break
        else:
          print("Invalid choice. Please try again.")
    
    mqtt_client = connect_to_mqtt()
    mqtt_client.greeting = for_present_greetings()
    mqtt_client.publish(Topic_For_Greeting, mqtt_client.greeting)
    print("The current published greeting: ", mqtt_client.greeting)

    while True:
        for_current_time(mqtt_client)
        brand_new_greeting = for_present_greetings()
        if brand_new_greeting != mqtt_client.greeting:
            mqtt_client.greeting = brand_new_greeting
            mqtt_client.publish(Topic_For_Greeting, brand_new_greeting)
            print("Published new greeting: ", brand_new_greeting)
        time.sleep(60)
 
# Written by Fernando Campos on 31/03/2024

# Define serial port and baud rate (match Arduino settings)
ser = serial.Serial('COM5', 9600) # Port where Aduino Board is connected  

# Roboflow Model details 
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="YOUR_API_KEY")
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


def mqtt_publish(ip="192.168.43.146", port=1883):
    file = open("picture.jpg", "rb")
    payload = file.read()
    client = paho.Client(paho.CallbackAPIVersion1, "smart_camera")
    client.connect(ip, port)
    client.publish("obj-rec", payload)
    client.disconnect()


def main():
    while True:
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

