# Written by Fernando Campos on 02/04/2024

# Maverick-Integrative-Project
Smart Camera: “The Companion Device”

# Smart Camera Project

# Overview
The Smart Camera Project is an innovative solution designed to leverage the power of IoT and AI for enhanced surveillance and object recognition capabilities. Utilizing a combination of hardware sensors, MQTT for communication, and integration with Roboflow for AI-powered object detection, this project offers a robust framework for various applications including security monitoring, wildlife observation, and more.

# Features
- **Motion Detection**: Utilizes PIR and other sensors to detect motion in the camera's vicinity.
- **Environmental Awareness**: Measures light and sound levels to optimize camera triggering conditions.
- **Distance Sensing**: Employs ultrasonic sensors to gauge the distance of objects or movement.
- **Dynamic Object Recognition**: Integrates with Roboflow AI to identify and classify objects within the camera's field of view.
- **MQTT Communication**: Leverages MQTT protocol for efficient message passing between the camera system and the server.
- **User Management**: Supports user authentication, subscription management, and personalized settings.

# Hardware Requirements
- Arduino board (or compatible microcontroller)
- PIR motion sensor
- Light sensor
- Sound sensor
- Ultrasonic distance sensor
- Webcam or compatible camera module
- Necessary cables and power supply

# Software and Libraries
- Arduino IDE for sensor data acquisition and control logic
- Python for the server-side MQTT broker and object recognition processing
- Paho MQTT Python library
- OpenCV Python library for image processing
- InferenceSDK for connecting to Roboflow
- SQLite for user management and data storage

# Installation and Setup
1. **Sensor Setup**: Connect the sensors to the Arduino according to the schematic provided in the `sensors_diagram` folder.
2. **Arduino Sketch**: Upload the Arduino sketch from the `arduino_code` folder to the microcontroller.
3. **Server Setup**: Ensure Python is installed on your server or development machine. Install required Python libraries with `pip install -r requirements.txt` from the `server_code` folder.
4. **MQTT Broker**: Set up your MQTT broker, noting the IP address and port for client connection. Adjust the connection settings in the Python and Arduino scripts accordingly.
5. **Roboflow Account**: Create an account at Roboflow, create a project, and note your API key and model ID for object detection.

# Usage
1. Power up the Arduino and sensors setup. Ensure it's connected to the same network as your MQTT broker.
2. Run the MQTT broker on your server or use an existing MQTT broker service.
3. Start the server script in the `server_code` folder to begin listening for sensor data and to process images through Roboflow.
4. Once motion is detected and conditions are met, the camera captures an image, sends it for object recognition, and publishes the results to an MQTT topic.

## Contributing
Contributions to the Smart Camera Project are welcome! Please review the contributing guidelines in `CONTRIBUTING.md` for more information on how to submit pull requests, report bugs, and suggest enhancements.

# License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.

---

Remember to replace placeholder text with your specific project details, paths, and configurations. This template aims to provide a solid starting point for documenting your project on GitHub.
