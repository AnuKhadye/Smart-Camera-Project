// Written by Fernando Campos on 12/03/2024

// Define the Trigger and Echo pin connections
const int trigPin = 3;
const int echoPin = 4;

void setup() {
  // Initialize Serial Monitor
  Serial.begin(9600);
  // Define sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  long duration, cm;

  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance
  cm = microsecondsToCentimeters(duration);

  // Print the distance in centimeters
  Serial.print(cm);
  Serial.println(" cm");

  // Delay a bit before the next measurement
  delay(250);
}

long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 343 meters per second or
  // 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}
