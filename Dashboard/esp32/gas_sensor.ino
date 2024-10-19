#include <Arduino.h>

const int gasSensorPin = 34;  // Assuming you're using GPIO 34 for the gas sensor

void setup() {
  Serial.begin(115200);
  pinMode(gasSensorPin, INPUT);
}

void loop() {
  int gasValue = analogRead(gasSensorPin);
  Serial.println(gasValue);  // Send the gas sensor value via serial
  delay(1000);  // Adjust the delay as per your requirement
}
