// Written by Fernando Campos 11/03/2024

int pirPin = 2; // Connect HC-SR501 OUT pin to Portenta H7 pin D2
int pirState = LOW; // Initialize variable to hold the PIR status
int lastPirState = LOW; // Stores the last state of the PIR sensor

void setup() {
  Serial.begin(9600); // Start Serial communication
  pinMode(pirPin, INPUT); // Set the pin as input
  Serial.println("PIR Motion Sensor Test");
}

void loop() {
  pirState = digitalRead(pirPin); // Read the state of the PIR sensor

  // Only print when the state changes
  if (pirState != lastPirState) {
    if (pirState == HIGH) {
      Serial.println("Motion detected!");
    } else {
      Serial.println("No motion");
    }
    lastPirState = pirState; // Update the last state
  }
  delay(100); // Shorter delay to make the loop more responsive
}
