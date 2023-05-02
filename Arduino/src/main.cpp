#include <Arduino.h>

// Motor A connections
int enA = 6;
int in1 = 7;
int in2 = 8;
// Motor B connections
int enB = 5;
int in3 = 3;
int in4 = 4;

int baseSpeed = 200;
int leftmotorSpeed = 0;
int rightmotorSpeed = 0;

void stop(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);

  analogWrite(enA, 0);
  analogWrite(enB, 0);
}

void turnMotors(int leftMotorSpeed, int rightMotorSpeed) {
    
    if(leftMotorSpeed > 0) {
        analogWrite(enA, leftMotorSpeed + baseSpeed);   
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
    } else {
        analogWrite(enA, -leftMotorSpeed + baseSpeed);
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
    }

    if(rightMotorSpeed > 0){
        analogWrite(enB, rightMotorSpeed + baseSpeed);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
    } else {
        analogWrite(enB, -rightMotorSpeed + baseSpeed);
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
    }

}

void moveMotors(int advanceSpeed, int turnSpeed){

    leftmotorSpeed = advanceSpeed + turnSpeed;
    rightmotorSpeed = advanceSpeed - turnSpeed;

    turnMotors(leftmotorSpeed, rightmotorSpeed);

    delay(10);
}


void setup() {
	// Set all the motor control pins to outputs
	pinMode(enA, OUTPUT);
	pinMode(enB, OUTPUT);
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	pinMode(in3, OUTPUT);
	pinMode(in4, OUTPUT);
	
	// Turn off motors - Initial state
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	digitalWrite(in3, LOW);
	digitalWrite(in4, LOW);

  Serial.begin(9600);
}

void loop() {

	
  for(int i = 0; i < 50; i++) {
    moveMotors(i, 0);
    Serial.println("Avanzando");
    delay(20);
  }
  delay(2000);

  /*
  for(int i = 0; i > -50; i--) {
    moveMotors(i, 0);
    Serial.println("Indietreggiando");
    delay(20);
  }

  for(int i = 0; i < 10; i++) {
    moveMotors(0, i);
    Serial.println("Sinistra");
    delay(100);
  }

  for(int i = 0; i < 10; i++) {
    moveMotors(0, -i);
    Serial.println("Destra");
    delay(100);
  }
  */

  stop();

  delay(1000);

}
