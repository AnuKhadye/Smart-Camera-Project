// Written by Fernando Campos on 26/03/2026

#include "arducam_dvp.h"
#include "Arduino_H7_Video.h"
#include "dsi.h"
#include "SDRAM.h"

// This example assumes a grayscale camera (adjust based on the model)
#define ARDUCAM_CAMERA_OV767X
#define IMAGE_MODE CAMERA_GRAYSCALE

#ifdef ARDUCAM_CAMERA_OV767X
#include "OV7670/ov767x.h"
OV7675 ov767x;
Camera cam(ov767x);
#endif

// Frame buffers
FrameBuffer fb;
FrameBuffer outfb;  // Not used in this example (optional for processing)

// The buffer used to store the captured image data (adjust size if needed)
uint8_t captured_image_data[640 * 480]; // Example buffer, adjust based on image size

// Sensor pins
int motionSensorPin = 2;
int lightSensorPin = A1;
int distanceTrigPin = 3;
int distanceEchoPin = 4;
int micPin = A0;

// Thresholds and conditions
int lightThresholdMin = 300;
int lightThresholdMax = 700;
long distanceMin = 200; // Minimum distance in cm (2 meters)
long distanceMax = 1500; // Maximum distance in cm (15 meters)
int soundThreshold = 700;

// Flags and timeout
bool capture_image = false;
const int capture_timeout = 3000; // milliseconds

Arduino_H7_Video Display(800, 480, GigaDisplayShield);

void blinkLED(uint32_t count = 0xFFFFFFFF) {
  pinMode(LED_BUILTIN, OUTPUT);
  while (count--) {
    digitalWrite(LED_BUILTIN, LOW);
    delay(50);
    digitalWrite(LED_BUILTIN, HIGH);
    delay(50);
  }
}

// Sensor implementations
bool checkMotion() {
  // Example: Returns true if motion is detected
  return digitalRead(motionSensorPin) == HIGH;
}

bool checkLightLevel() {
  int lightLevel = analogRead(lightSensorPin);
  // Adjust thresholds based on your sensor and lighting conditions
  return lightLevel >= lightThresholdMin && lightLevel <= lightThresholdMax;
}

bool checkSoundLevel() {
  int soundLevel = analogRead(micPin);
  // Adjust threshold based on your sensor and noise level
  return soundLevel > soundThreshold;
}

bool checkDistance() {
  digitalWrite(distanceTrigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(distanceTrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(distanceTrigPin, LOW);
  long duration = pulseIn(distanceEchoPin, HIGH);
  long distance = microsecondsToCentimeters(duration);
  // Adjust distance thresholds based on your sensor and desired range
  return distance >= distanceMin && distance <= distanceMax;
}

void setup() {
  // Init the cam (adjust resolution and frame rate if needed)
  if (!cam.begin(CAMERA_R320x240, IMAGE_MODE, 30)) {
    blinkLED();
  }

  // Display setup (optional for this example)
  Display.begin();

  // Sensor pin modes
  pinMode(motionSensorPin, INPUT);
  pinMode(lightSensorPin, INPUT);
  pinMode(distanceTrigPin, OUTPUT);
  pinMode(distanceEchoPin, INPUT);
  pinMode(micPin, INPUT);

  Serial.begin(9600);
  Serial.println("Camera and Sensors Initialized");
}

void loop() {
  // Sensor logic to trigger image capture
  if (checkMotion()) {
    Serial.println("Motion detected");
    if (checkLightLevel()) {
      Serial.println("Medium light level confirmed");
      if (checkDistance()) {
        Serial.println("Distance within range");
        if (!checkSoundLevel()) {
          Serial.println("Environment not loud, triggering camera");
          capture_image = true;
        } else {
          Serial.println("Environment too loud, not triggering camera");
        }
      }
    }
  }

  if (capture_image) {
  if (cam.grabFrame(fb, capture_timeout) == 0) {
    // Image capture successful
    Serial.println("Image captured!");

    // Copy captured image data to a separate buffer
    memcpy(captured_image_data, fb.getBuffer(), fb.getSize());

    // Base64 encoding and serial transmission
    int image_size = fb.getSize();
    char* encoded_data = new char[encode_base64_length(image_size)];  // Adjust size if needed
    int encoded_length = encode_base64((unsigned char*)captured_image_data, image_size, (unsigned char*)encoded_data);
    encoded_image = String(encoded_data, encoded_length);
    Serial.print("Sending image (base64 encoded): ");
    Serial.println(encoded_image);
    delete[] encoded_data;
  } else {
    Serial.println("Failed to capture image!");
  }
}

