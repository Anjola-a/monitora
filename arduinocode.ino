//FSR imports
#include <Wire.h>
#include "BluetoothSerial.h"

#define FORCE_SENSOR_PIN 38 // ESP32 pin GIOP36 (ADC0): the FSR and 10K pulldown are connected to A0
#define FORCE_SENSOR_PIN2 35 // ESP32 pin GIOP36 (ADC0): the FSR and 10K pulldown are connected to A0
#define FORCE_SENSOR_PIN3 37 // ESP32 pin GIOP36 (ADC0): the FSR and 10K pulldown are connected to A0

//#define FORCE_SENSOR_PIN 38 // ESP32 pin GIOP36 (ADC0): the FSR and 10K pulldown are connected to A0

//BNO055 imports
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
BluetoothSerial SerialBT;
int readings[] = {0, 0, 0};
int ranges[] = {0, 0, 0};
long randNumber;
int counter = 0;
int total = 0;
int total3 = 0;
int total2 = 0;
int temp;
int currentMillis = millis();
int startMillis = millis();


#define BNO055_SAMPLERATE_DELAY_MS (1000)
float x_accel_f = 0;
float y_accel_f = 0;
float z_accel_f = 0;
float x_accel = 0;
float y_accel = 0;
float z_accel = 0;
float time_change = 0;
int stime = 0;
int crtime = 0;
bool walking = false;
bool cstate = false;
bool movement = false;
int cnt = 0;
Adafruit_BNO055 bno = Adafruit_BNO055(55);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");
  IMU_setup();
}

void IMU_setup() {
  Wire.begin();
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }
  delay(1000);
  bno.setExtCrystalUse(true);
}

void loop() {
  //  initializing sensors
  imu::Vector<3> accel_value = bno.getVector(Adafruit_BNO055::VECTOR_ACCELEROMETER);
  int analogReading = analogRead(FORCE_SENSOR_PIN);
  int analogReading2 = analogRead(FORCE_SENSOR_PIN2);
  int analogReading3 = analogRead(FORCE_SENSOR_PIN3);

  //filter for IMU
  cnt ++;
  x_accel += abs(accel_value.x());
  y_accel += abs(accel_value.y());
  z_accel += abs(accel_value.z());

  if (cnt > 2) {
    x_accel_f = x_accel / 3;
    y_accel_f = y_accel / 3;
    z_accel_f = z_accel / 3;
    x_accel = 0;
    y_accel = 0;
    z_accel = 0;
    cnt = 0;
  }
  Serial.print("X accel: ");
  Serial.print(x_accel_f);
  Serial.print("Y accel: ");
  Serial.print(y_accel_f);
  Serial.print("Z accel: ");
  Serial.println(z_accel_f);
//  if (movement == false && (z_accel_f > 3.0 || x_accel_f > 1.7 ||y_accel_f > 10.1 || y_accel_f < 8.9 )) {
    if (movement == false && (x_accel_f > 1.1 || y_accel_f > 10.1 || y_accel_f < 8.9 || z_accel_f > 2.4)) {
    stime = millis();
    movement = true;
    Serial.println("movement true first");
//    Serial.println("FSR OFF");
  }
    if (movement == true && (x_accel_f > 1.1 || y_accel_f > 10.1 || y_accel_f < 8.9 || z_accel_f > 2.4)) {
    crtime = millis();
    Serial.println("movement true second");
//    Serial.println("FSR OFF");
    if (crtime - stime > 5000) {
      walking = true;
      Serial.println("FSR ON");
    }
  } else {
    movement = false;
    walking = false;
  }

  //  logic for moving average filer for FSR  
  counter ++;
  total += analogReading;
  total2 += analogReading2;
  total3 += analogReading3;
  //a window greater than 2 slows down the
  //code and will not enough data points
  if (counter > 1) {
    readings[0] = total / 2;
    readings[1] = total2 / 2;
    readings[2] = total3 / 2;
    total = 0;
    total2 = 0;
    total3 = 0;
    counter = 0;
  }


  for (int thisFSR = 0; thisFSR < 3; thisFSR++) {
    if (readings[thisFSR] < 10) {      // from 0 to 9
      ranges[thisFSR] = 0;
    }
    else if  (readings[thisFSR] < 200) { // from 10 to 199
      ranges[thisFSR] = 1;
    }
    else if (readings[thisFSR] < 400) {// from 200 to 399
      ranges[thisFSR] = 2;

    } else if (readings[thisFSR] < 600) { // from 400 to 699
      ranges[thisFSR] = 3;
    }
    else if (readings[thisFSR] < 800) { // from 700 to 799
      ranges[thisFSR] = 4;
    }
    else if (readings[thisFSR] < 1000) { // from 700 to 799
      ranges[thisFSR] = 5;
    }
    else if (readings[thisFSR] < 1200) { // from 700 to 799
      ranges[thisFSR] = 6;
    }
    else if (readings[thisFSR] < 1400) { // from 700 to 799
      ranges[thisFSR] = 7;
    }
    else { // from 800 to 1023
//      Serial.println(readings[thisFSR]);
      ranges[thisFSR] = 8;
    }
  }
//  Serial.print("FSR1");
//  Serial.println(ranges[0]);
//  Serial.print("FSR2");
//  Serial.println(ranges[1]);
//  Serial.print("FSR3");
//  Serial.println(ranges[2]);
  
  if (walking == true) {
    SerialBT.print(ranges[0]);
    SerialBT.print(",");
    SerialBT.print(ranges[2]);
    SerialBT.print(",");
    SerialBT.println(ranges[1]);
    
//    SerialBT.println(filtered_reading);

//    Serial.print("FSR1");
    Serial.print(ranges[0]);
    Serial.print(",");
    Serial.print(ranges[2]);
    Serial.print(",");
    Serial.println(ranges[1]);
  }
  currentMillis = millis();
  temp = currentMillis - startMillis;
  //  Serial.println(temp);
  //  if (temp > 10000){
  //    delay(10000);
  //    startMillis = millis();
  //  }

  delay(300);
  }