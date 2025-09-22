void setup() {
    Serial.begin(9600);
    pinMode(5, OUTPUT);
}

void loop() {
    if(Serial.available() > 0){
      if(Serial.read() == '#'){
        String value = Serial.readStringUntil(';');
        int intValue = value.toInt();

        analogWrite(5, intValue);
      }
    }
}