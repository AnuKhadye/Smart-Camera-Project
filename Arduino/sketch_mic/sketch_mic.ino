// Written by Fernando Campos on 23/03/2024

const int micPin = A2; // Microphone Max4466 output connected to analog pin A2
int soundLevel;
int previousLevel = 0;
const int quietThreshold = 300; // Adjust these values based on your testing
const int loudThreshold = 700; // Adjust these values based on your testing

void setup() {
  Serial.begin(9600);
}

void loop() {
  soundLevel = analogRead(micPin);

  // Display the quantitative sound level
  Serial.print("Sound level: ");
  Serial.println(soundLevel);

  // Categorize and display the qualitative assessment
  if (soundLevel < quietThreshold) {
    Serial.println("Environment: Quiet");
  } else if (soundLevel >= quietThreshold && soundLevel < loudThreshold) {
    Serial.println("Environment: Moderate");
  } else if (soundLevel >= loudThreshold) {
    Serial.println("Environment: Loud");
  }

  // Detect and display significant changes in sound level
  if (abs(soundLevel - previousLevel) > 100) { // "100" is a placeholder for significant change
    if (soundLevel > previousLevel) {
      Serial.println("Getting louder");
    } else {
      Serial.println("Getting quieter");
    }
  }

  previousLevel = soundLevel;
  
  delay(500); // Adjust delay for more or less frequent readings
}
