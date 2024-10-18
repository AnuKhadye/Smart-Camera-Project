// Written by Fernando Campos on 23/03/2024

int lastReading = 0; // Store the last light sensor reading
String lastStatus = ""; // Store the last status message

String getLightLevelDescription(int reading) {
  const int DARK_THRESHOLD = 341;
  const int LIGHT_THRESHOLD = 682;
  const int SIGNIFICANT_CHANGE = 50; // Define what you consider a significant change
  String status = "";

  if (reading <= DARK_THRESHOLD) {
    status = "Dark.";
  } else if (reading > DARK_THRESHOLD && reading <= LIGHT_THRESHOLD) {
    status = "Medium Light.";
  } else {
    status = "Bright.";
  }

  // Check if the change is significant to update the qualitative status
  if (abs(reading - lastReading) >= SIGNIFICANT_CHANGE) {
    if (reading < lastReading) {
      status += " It is getting darker.";
    } else if (reading > lastReading) {
      status += " It is getting lighter.";
    }
    lastReading = reading; // Update lastReading for the next comparison
  }
  // Always update lastStatus with the current status
  lastStatus = status;
  return status;
}

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  int reading = analogRead(A1); // Assuming your light sensor is connected to A0
  String description = getLightLevelDescription(reading);
  Serial.print("Reading: ");
  Serial.print(reading);
  Serial.print(" - ");
  Serial.println(description);
  delay(1000); // Adjust the delay as needed
}
