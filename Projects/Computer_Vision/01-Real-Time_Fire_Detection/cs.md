> ## 4.4.2 Arduino Code 

```cpp
#include <PID_v1.h>  
#include <LMotorController.h>  
#include "I2Cdev.h"  
#include "MPU6050_6Axis_MotionApps20.h"  
#include "Wire.h"  
#define MIN_SPEED 30  
MPU6050 sensor;  
// Sensor state variables 
bool isDmpReady = false; // true if DMP initialization is successful  
uint8_t interruptStatus; // stores the interrupt status byte from the sensor  
uint8_t deviceStatus; // stores the status after device operations (0 = success, non-zero = error) 
uint16_t expectedPacketSize; // expected DMP packet size (default: 42 bytes)  
uint16_t currentFifoCount; // byte count currently in the FIFO buffer  
uint8_t fifoData[64]; // FIFO data storage  
// Motion data variables 
Quaternion orientation; // quaternion data [w, x, y, z]  
VectorFloat gravityVector; // gravity vector [x, y, z] 
float angles[3]; // [yaw, pitch, roll] container and gravity vector 
// PID control variables 
double targetAngle = 181.0, currentAngle = targetAngle, angleOffset = 0.1, pidInput, pidOutput, proportionalGain = 60, derivativeGain = 2.2, integralGain = 270;
PID pidController(&pidInput, &pidOutput, &currentAngle, proportionalGain, integralGain, derivativeGain, DIRECT);  
// Motor control factors 
double leftMotorSpeedFactor = 0.5, rightMotorSpeedFactor = 0.5;   
// Motor driver pins 
int motorPinENA = 12, motorPinIN1 = 8, motorPinIN2 = 9, motorPinIN3 = 10, motorPinIN4 = 11, motorPinENB = 13;
// Initialize motor controller 
LMotorController motorControl(motorPinENA, motorPinIN1, motorPinIN2, motorPinENB, motorPinIN3, motorPinIN4, leftMotorSpeedFactor, rightMotorSpeedFactor);  
volatile bool isSensorInterrupt = false; // indicates if the MPU interrupt pin is triggered  
// Interrupt function for DMP data ready 
void onDmpDataReady() { 
  isSensorInterrupt = true; 
} 

void setup() { 
  // Initialize I2C communication 
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE  
    Wire.begin();  
    TWBR = 24; // 400kHz I2C clock  
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE  
    Fastwire::setup(400, true);  
  #endif  
  sensor.initialize();  
  deviceStatus = sensor.dmpInitialize();  
  // Gyro and accelerometer offset values (customize for your sensor) 
  sensor.setXGyroOffset(0);  
  sensor.setYGyroOffset(0);  
  sensor.setZGyroOffset(0);  
  sensor.setZAccelOffset(0); // Default value for testing 
  // Check if initialization succeeded 
  if (deviceStatus == 0) { 
    sensor.setDMPEnabled(true);  
    attachInterrupt(0, onDmpDataReady, RISING);  
    interruptStatus = sensor.getIntStatus();  
    isDmpReady = true;  
    expectedPacketSize = sensor.dmpGetFIFOPacketSize();  
    // Configure PID controller 
    pidController.SetMode(AUTOMATIC);  
    pidController.SetSampleTime(10);  
    pidController.SetOutputLimits(-255, 255);  
  } else { 
    Serial.print(F("DMP Initialization failed (code "));  
    Serial.print(deviceStatus);  
    Serial.println(F(")")); 
  } 
} 

void loop() { 
  if (!isDmpReady) return; 
  // Wait for MPU interrupt or additional data packets 
  while (!isSensorInterrupt && currentFifoCount < expectedPacketSize) { 
    // No new data - perform PID control and send output to motors 
    pidController.Compute();  
    motorControl.move(pidOutput, MIN_SPEED); 
  } 
  // Reset interrupt flag and get interrupt status 
  isSensorInterrupt = false;  
  interruptStatus = sensor.getIntStatus();  
  currentFifoCount = sensor.getFIFOCount();  
  // Check for FIFO overflow or other errors 
  if ((interruptStatus & 0x10) || currentFifoCount == 1024) { 
    sensor.resetFIFO();  
    Serial.println(F("FIFO overflow!")); 
  } else if (interruptStatus & 0x02) { 
    while (currentFifoCount < expectedPacketSize)  
      currentFifoCount = sensor.getFIFOCount();  
    // Read a packet from FIFO 
    sensor.getFIFOBytes(fifoData, expectedPacketSize);  
    currentFifoCount -= expectedPacketSize;  
    sensor.dmpGetQuaternion(&orientation, fifoData);  
    sensor.dmpGetGravity(&gravityVector, &orientation);  
    sensor.dmpGetYawPitchRoll(angles, &orientation, &gravityVector);  
    pidInput = angles[1] * 180 / M_PI + 180; // Convert pitch angle to inp for PID 
  } 
}
```