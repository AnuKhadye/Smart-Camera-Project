# Improved Image Transfer Script using MQTT

import paho.mqtt.client as mqtt

# Define connection details
broker = 'broker.mqtt.cool'
port = 1883
topic = "ph174"
client_id = 'your_unique_client_id'

# Error handling function
def handle_error(rc):
    if rc == 0:
        print("Successfully connected to MQTT Broker!")
    else:
        print(f"Connection error: {rc}")

# Connect to MQTT Broker
def connect_mqtt():
    client = mqtt.Client(client_id=client_id)
    client.on_connect = handle_error
    client.connect(broker, port)
    return client

# Publish image data
def publish_image(client):
    try:
        # Open image file in binary read mode
        with open("./vv1.jpg", 'rb') as image_file:
            image_data = image_file.read()

        # Publish image data to specified topic with QoS level 2
        result = client.publish(topic, image_data, qos=2)
        msg_status = result[0]

        if msg_status == 0:
            print(f"Image sent successfully to topic: {topic}")
        else:
            print(f"Failed to send image: Error code {msg_status}")
    except FileNotFoundError:
        print(f"Error: Image file 'vv1.jpg' not found!")

# Main program loop
def main():
    client = connect_mqtt()
    client.loop_start()  # Start network loop in a separate thread
    publish_image(client)
    time.sleep(5)  # Wait for message delivery (adjust as needed)
    client.loop_stop()  # Stop network loop
    client.disconnect()  # Disconnect from broker

if __name__ == '__main__':
    main()
