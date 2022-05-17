// Include the required Arduino libraries:
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 13

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensor(&oneWire);

void setup() {
  Serial.begin(9600) ;
  sensor.begin();
}

void loop() {
  sensor.requestTemperatures();
  delay(5000);
  float tempC = sensor.getTempCByIndex(0); 
  Serial.print(tempC);
}
