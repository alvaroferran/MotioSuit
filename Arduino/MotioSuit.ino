//--------------------------------------------------------------
//--    MotioSuit
//--    IMU based motion capture suit
//--------------------------------------------------------------
//--    BQ
//--------------------------------------------------------------
//--    Created by 
//--        Alvaro Ferran (alvaroferran)
//--------------------------------------------------------------
//--    Released on January 2016
//--    under the GPL v2
//--------------------------------------------------------------
#include "BNO055.h"
#include "I2CMux.h"
#include <Wire.h>

#define I2CMux_ADDR 0x70 
#define BNO055_ADDR_A 0x28
#define BNO055_ADDR_B 0x29

I2CMux mux(I2CMux_ADDR);

BNO055 sensorA(BNO055_ADDR_A), sensorB(BNO055_ADDR_B);

BNO055  bus1Sensor[]={sensorA},
        bus2Sensor[]={sensorA,sensorB};

BNO055 *tree[]={
    bus2Sensor,
    bus2Sensor,
    bus1Sensor,
    bus2Sensor,
    //bus2Sensor,
    //bus2Sensor,
    //bus2Sensor,
    bus2Sensor};

int sizeB=sizeof(BNO055);
int size1=sizeof(bus1Sensor);
int size2=sizeof(bus2Sensor);

int numberOfSensorsInBus[]={
    size2/sizeB,
    size2/sizeB,
    size1/sizeB,
    size2/sizeB,
    //size2/sizeB,
    //size2/sizeB,
    //size2/sizeB,
    size2/sizeB};

int numberOfBuses=sizeof(tree)/sizeof(int);

float q0, q1, q2, q3;


void setup(){
    Wire.begin();
    Serial.begin(115200);
    Serial.flush();
    Serial.println("starting");
    for(int i=0; i<numberOfBuses;i++){
            mux.switchToBus(i);
        for(int j=0; j< numberOfSensorsInBus[i] ; j++){
            tree[i][j].init();
            Serial.print("sensor ");
            Serial.print(i);
            Serial.print(" , ");
            Serial.println(j);
        }
    }
    delay(1000);
    Serial.println("Started");
}


void loop(){
    if(Serial.available()){
        if(Serial.read()=='a'){
            for(int i = 0; i<numberOfBuses;i++){
                mux.switchToBus(i);
                for(int j=0; j<numberOfSensorsInBus[i]; j++){
                    
                    tree[i][j].readQuat();

                    q0=tree[i][j].quat.q0;
                    q1=tree[i][j].quat.q1;
                    q2=tree[i][j].quat.q2;
                    q3=tree[i][j].quat.q3;
 
                    Serial.print(q0,2);
                    Serial.print(",");
                    Serial.print(q1,2);
                    Serial.print(",");
                    Serial.print(q2,2);
                    Serial.print(",");
                    Serial.print(q3,2);
                    Serial.print(";");            
                    
                }
            }   
        Serial.println("");
        }      
    }
}