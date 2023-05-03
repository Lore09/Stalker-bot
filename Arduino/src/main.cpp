#include <Arduino.h>

#define DEBUG 1

// Motor A connections
int enA = 6;
int in1 = 7;
int in2 = 8;
// Motor B connections
int enB = 5;
int in3 = 4;
int in4 = 3;


// Motor control variables
int baseSpeed = 100;  // Base PWM value to sent to motors (Range 0-255), adjust to match your motors
bool new_data = false; // Flag to indicate new data from serial communication

int turnTarget = 0; // Target value for turning (Range -255 to 255)
int currentTurn = 0; // Current turning value (Range -255 to 255)

int advanceTarget = 0; // Target value for advancing (Range -255 to 255)
int currentAdvance = 0; // Current advancing value (Range -255 to 255)

int leftMotorSpeed = 0;  // PWM value for left motor (Range 0 to 255)
int rightMotorSpeed = 0; // PWM value for right motor (Range 0 to 255)

// Servo control variables
int servoTarget = 0; // Target value for servo (Range 0 to 180)
int servoAngle = 0; // Current angle of servo (Range 0 to 180)

void stop(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);

  analogWrite(enA, 0);
  analogWrite(enB, 0);

  currentTurn = 0;
  currentAdvance = 0;
  advanceTarget = 0;
  turnTarget = 0;
}

void moveMotors(int advanceSpeed, int turnSpeed){

    leftMotorSpeed = advanceSpeed + turnSpeed;
    rightMotorSpeed = advanceSpeed - turnSpeed;

    if(leftMotorSpeed == 0 && rightMotorSpeed == 0) {
      stop();
      return;
    }

    if(leftMotorSpeed > 0) {
        analogWrite(enA, leftMotorSpeed + baseSpeed);   
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
    } else{
        analogWrite(enA, -(leftMotorSpeed + baseSpeed));
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
    }

    if(rightMotorSpeed > 0){
        analogWrite(enB, rightMotorSpeed + baseSpeed);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
    } else {
        analogWrite(enB, -(rightMotorSpeed + baseSpeed));
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
    }

}

void turnLeft(){
  moveMotors(0, 50);
}

void turnRight(){
  moveMotors(0, -50);
}

void advance(){
  moveMotors(50, 0);
}

void back(){
  moveMotors(-50, 0);
}


bool checkSerialData(){
  // Read data from Serial Communication
  if (Serial.available() > 0) {
    
    String data = Serial.readStringUntil('\n');

    // split value,value,value by comma
    int firstComma = data.indexOf(',');
    int secondComma = data.indexOf(',', firstComma + 1);

    // get advance and turn values
    advanceTarget = data.substring(0, firstComma).toInt();
    turnTarget = data.substring(firstComma + 1, secondComma).toInt();
    servoTarget = data.substring(secondComma + 1).toInt();

    return true;
  }
  else return false;
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
	stop();

  // Begin serial communication at a baudrate of 9600:
  Serial.begin(9600);

  delay(1000);
}

void loop() {
    
	if(checkSerialData()){
    // Reset current values
    currentTurn = 0;
    currentAdvance = 0;

    new_data = true;
  };

  // move towards target values
  if(new_data && (currentTurn != turnTarget || currentAdvance != advanceTarget)){
    // turn towards target
    if(currentTurn != turnTarget){
      if(currentTurn < turnTarget) currentTurn++;
      else currentTurn--;
    }

    // advance towards target
    if(currentAdvance != advanceTarget){
      if(currentAdvance < advanceTarget) currentAdvance++;
      else currentAdvance--;
    }

    moveMotors(currentAdvance, currentTurn);
  }
  else if(new_data){
    stop();
    new_data = false;
    Serial.println("STOP");
  }

  //---------------------------------
  // TEST
  advance();
  //---------------------------------


  // Debug data
  if(DEBUG){
    Serial.print("Advance: ");
    Serial.print(currentAdvance);
    Serial.print(" Turn: ");
    Serial.print(currentTurn);
    Serial.print(" Servo: ");
    Serial.println(servoTarget);
  }

  delay(10);

}
