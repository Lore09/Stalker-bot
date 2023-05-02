#include <string.h>

void setup() {
  Serial.begin(9600);
}
void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    if (data == "ON"){
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("LED ON");
      }
    else if(data == "OFF"){
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED OFF");
    }
    else{
      Serial.println(data);
    }
  }
}
