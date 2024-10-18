// Written by Fernando Campos on 21/03/2024

#include <Wire.h>

// OV5642 I2C address (Change if different)
#define CAMERA_I2C_ADDRESS 0x3C

void setup() {
  Serial.begin(115200);
  Wire.begin(); // Initializes the default I2C bus
  while (!Serial); // Wait for the serial monitor to open
  
  Serial.println("Initializing I2C communication with OV7056...");

  // Reading the high byte of the chip ID as an example
  Wire.beginTransmission(CAMERA_I2C_ADDRESS);
  Wire.write(0x30); // MSB of the address
  Wire.write(0x0A); // LSB of the address
  Wire.endTransmission(false);

  Wire.requestFrom(CAMERA_I2C_ADDRESS, 2); // Request 2 bytes
  if (Wire.available() == 2) {
    uint8_t msb = Wire.read(); // Read MSB
    uint8_t lsb = Wire.read(); // Read LSB
    uint16_t chipID = (msb << 8) | lsb;

    Serial.print("Chip ID: 0x");
    Serial.println(chipID, HEX);
  } else {
    Serial.println("Failed to read from the camera.");
  }
}

void loop() {
  // Do nothing here
}
