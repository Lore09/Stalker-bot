#include <Arduino.h>

#define DEBUG 0

// Motor A connections
int enA = 6;
int in1 = 7;
int in2 = 8;
// Motor B connections
int enB = 5;
int in3 = 4;
int in4 = 3;


// Motor control variables
int base_pwm = 100;  // Base PWM value to sent to motors (Range 0-255), adjust to match your motors

int turn_speed = 0; // Target value for turning (Range -255 to 255)

int advance_speed = 0; // Target value for advancing (Range -255 to 255)

int leftMotorSpeed = 0;  // PWM value for left motor (Range 0 to 255)
int rightMotorSpeed = 0; // PWM value for right motor (Range 0 to 255)

long command_start_time = 0; // Time of last command
long command_duration = 0; // Duration of last command

// Servo control variables
//int servoTarget = 0; // Target value for servo (Range 0 to 180)
//int servoAngle = 0; // Current angle of servo (Range 0 to 180)

void stop(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);

  analogWrite(enA, 0);
  analogWrite(enB, 0);

}

void moveMotors(int advanceSpeed, int turnSpeed){

    rightMotorSpeed = advanceSpeed + turnSpeed;
    leftMotorSpeed = advanceSpeed - turnSpeed;

    if(leftMotorSpeed == 0 && rightMotorSpeed == 0) {
      stop();
      return;
    }

    if(leftMotorSpeed > 0) {
        analogWrite(enA, leftMotorSpeed + base_pwm);   
        digitalWrite(in1, HIGH);
        digitalWrite(in2, LOW);
    } else{
        analogWrite(enA, -(leftMotorSpeed - base_pwm));
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);
    }

    if(rightMotorSpeed > 0){
        analogWrite(enB, rightMotorSpeed + base_pwm);
        digitalWrite(in3, HIGH);
        digitalWrite(in4, LOW);
    } else {
        analogWrite(enB, -(rightMotorSpeed - base_pwm));
        digitalWrite(in3, LOW);
        digitalWrite(in4, HIGH);
    }

}

void turnLeft(){
  moveMotors(0, 50);
  delay(400);
}

void turnRight(){
  moveMotors(0, -50);
  delay(400);
}

void advance(){
  moveMotors(50, 0);
  delay(800);
}

void back(){
  moveMotors(-50, 0);
  delay(800);
}


bool checkSerialData(){
  // Read data from Serial Communication
  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\n');

    // Direct commands
    switch (data[0])
    {
    case 'A':
      advance();
      turn_speed=0;
      advance_speed=0;
      break;
    
    case 'B':
      back();
      turn_speed=0;
      advance_speed=0;
      break;
    
    case 'L':
      turnLeft();
      turn_speed=0;
      advance_speed=0;
      break;
    
    case 'R':
      turnRight();
      turn_speed=0;
      advance_speed=0;
      break;
    
    case 'S':
      stop();
      turn_speed=0;
      advance_speed=0;
      break;
    
    // Specific data
    default:
      // split value,value,value by comma
      int firstComma = data.indexOf(',');
      int secondComma = data.indexOf(',', firstComma + 1);

      // get advance and turn values
      advance_speed = data.substring(0, firstComma).toInt();
      turn_speed = data.substring(firstComma + 1, secondComma).toInt();
      command_duration = data.substring(secondComma + 1).toInt();
      break;
    }

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
    command_start_time = millis();
  };

  // Move motors
  if(millis() - command_start_time < command_duration){
    moveMotors(advance_speed, turn_speed);
  }
  else {
    stop();
    Serial.println("STOP");
  }

  // Debug data
  if(DEBUG){
    Serial.print("Left Motor: ");
    Serial.print(leftMotorSpeed);
    Serial.print(" Right Motor: ");
    Serial.println(rightMotorSpeed);
    //Serial.print(" Servo: ");
    //Serial.println(servoTarget);
  }

  delay(10);
}
