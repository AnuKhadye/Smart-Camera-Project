// Written by Fernando Campos on 26/03/2024

#include <SPI.h>
#include <Wire.h>

// Define sensor pins
int motionSensorPin = A1;  // Example pin for PIR sensor
int lightSensorPin = A2;    // Light sensor
int distanceTrigPin = A3;    // Ultrasonic sensor Trigger pin
int distanceEchoPin = A4;   // Ultrasonic sensor Echo pin
int soundSensorPin = A5;    // Sound sensor

// Camera trigger pin (if not applicable, remove the line)
int cameraTriggerPin = 10;

// Thresholds and conditions
int lightThresholdMin = 300; // Lower threshold for medium light level
int lightThresholdMax = 700; // Upper threshold for medium light level
long distanceMin = 200;      // Minimum distance in cm (2 meters)
long distanceMax = 1500;     // Maximum distance in cm (15 meters)
int soundThreshold = 700;     // Sound level threshold for "loud"

// Function prototypes
bool checkMotion();
bool checkLightLevel();
bool checkDistance();
bool checkSoundLevel();
void triggerCamera();
long microsecondsToCentimeters(long microseconds);

void setup() {
  Serial.begin(9600);
  pinMode(motionSensorPin, INPUT);
  pinMode(lightSensorPin, INPUT);
  pinMode(distanceTrigPin, OUTPUT);
  pinMode(distanceEchoPin, INPUT);
  pinMode(soundSensorPin, INPUT);
  pinMode(cameraTriggerPin, OUTPUT); // Set camera trigger pin as output 

  Serial.println("System Ready");
}

void loop() {
  if (checkMotion()) {
    Serial.println("Motion detected");
    if (checkLightLevel()) {
      Serial.println("Medium light level confirmed");
      if (checkDistance()) {
        Serial.println("Distance within range");
        if (!checkSoundLevel()) {
          Serial.println("Environment not loud, triggering camera");
          triggerCamera();
        } else {
          Serial.println("Environment too loud, not triggering camera");
        }
      }
    }
  }
  delay(1000); // It can be adjusted based on the needs
}

bool checkMotion() {
  // Example: Returns true if motion is detected
  return digitalRead(motionSensorPin) == HIGH;
}

bool checkLightLevel() {
  int lightLevel = analogRead(lightSensorPin);
  return lightLevel >= lightThresholdMin && lightLevel <= lightThresholdMax;
}

bool checkDistance() {
  digitalWrite(distanceTrigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(distanceTrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(distanceTrigPin, LOW);
  long duration = pulseIn(distanceEchoPin, HIGH);
  long distance = microsecondsToCentimeters(duration);
  return distance >= distanceMin && distance <= distanceMax;
}

bool checkSoundLevel() {
  int soundLevel = analogRead(soundSensorPin);
  return soundLevel > soundThreshold;
}

void triggerCamera() {
  // Trigger camera using the defined pin (if applicable)
  digitalWrite(cameraTriggerPin, HIGH);
  delay(100); // Example delay
  digitalWrite(cameraTriggerPin, LOW);
}

long microsecondsToCentimeters(long microseconds) {
  return microseconds / 29 / 2;
}
