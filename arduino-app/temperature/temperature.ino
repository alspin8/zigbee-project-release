// Include the required Arduino libraries:
#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>

#define ONE_WIRE_BUS 13

SoftwareSerial XBee(0,1);


int value;
int val;

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensor(&oneWire);

void setup() {
  Serial.begin(9600) ;
  sensor.begin();
  XBee.begin(9600);
}

void loop() {
  sensor.requestTemperatures();
  delay(5000);
  float tempC = sensor.getTempCByIndex(0); 
  Serial.print("Température : ");
  Serial.println(tempC);
  Serial.println(XBee.available());
  if(XBee.available() > 0) {
    Serial.println("foo");
    XBee.write("foo");
  }
}
