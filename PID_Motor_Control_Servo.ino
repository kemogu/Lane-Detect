#include <Servo.h> 

#define rightREN 37
#define rightLEN 35
#define rightRPWM 4
#define rightLPWM 5
#define rightENC 2 

#define leftREN 31
#define leftLEN 33
#define leftRPWM 10
#define leftLPWM 9
#define leftENC 3



#define ServoMotor 12

Servo servoM;
int period=100;

int rightEncoderCountPerPeriod=0;
double desiredRightRPS=1;
double rightRPS=0;
double rightPID=0;
double Kp_r=15;
double Ki_r=100;
double Kd_r=0;
double rightIntegral=0;
double rightDerivative=0;

int leftEncoderCountPerPeriod=0;
double desiredLeftRPS=1;
double leftRPS=0;
double leftPID=0;
double Kp_l=15;
double Ki_l=100;
double Kd_l=0;
double leftIntegral=0;
double lefttDerivative=0;

unsigned long lastRPMCalculatingTime=0;

void setup() 
{
Serial.begin(9600);
servoM.attach(ServoMotor);

pinMode(rightREN,OUTPUT);
pinMode(rightLEN,OUTPUT);
pinMode(rightRPWM,OUTPUT);
pinMode(rightLPWM,OUTPUT);
pinMode(rightENC,INPUT);

pinMode(leftREN,OUTPUT);
pinMode(leftLEN,OUTPUT);
pinMode(leftRPWM,OUTPUT);
pinMode(leftLPWM,OUTPUT);
pinMode(leftENC,INPUT);

attachInterrupt(digitalPinToInterrupt(rightENC), ReadRightENC, RISING);
attachInterrupt(digitalPinToInterrupt(leftENC), ReadLeftENC, RISING);

digitalWrite(leftREN,HIGH);
digitalWrite(leftLEN,HIGH);
digitalWrite(rightREN,HIGH);
digitalWrite(rightLEN,HIGH);
}
int xx[2]={45,135};
int i=0;

void loop() {
  int pos;
  Serial.print(rightPID);
  Serial.print(",");
  Serial.println(leftPID);
    
  if(millis() - lastRPMCalculatingTime > period){
    calculateRPS();

    lastRPMCalculatingTime=millis();
    double errorRight=desiredRightRPS-rightRPS;
    double errorLeft=desiredLeftRPS-leftRPS;
    leftIntegral=leftIntegral + errorLeft * period/1000;
    rightIntegral=rightIntegral + errorRight * period/1000;

    rightPID = Kp_r*errorRight + Ki_r*rightIntegral ;
    leftPID = Kp_l*errorLeft + Ki_l*leftIntegral ;
    analogWrite(leftRPWM, leftPID);
    analogWrite(rightRPWM, rightPID);
    servoM.write(xx[i++%2]);
  } 
}


void ReadRightENC() 
{
  rightEncoderCountPerPeriod++;
}

void ReadLeftENC() 
{
  leftEncoderCountPerPeriod++;
}


void calculateRPS(){
  rightRPS=(double(rightEncoderCountPerPeriod)/224.4)*1000/(double)period;
  leftRPS=(double(leftEncoderCountPerPeriod)/224.4)*1000/(double)period;
  leftEncoderCountPerPeriod=0;
  rightEncoderCountPerPeriod=0;
}