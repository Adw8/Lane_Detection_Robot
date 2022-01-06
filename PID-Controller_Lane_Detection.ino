#include <Wire.h>

//define pin numbers for direction and pwm of motors
int IN_1 = 4;
int IN_2 = 2;
int IN_3 = 6;
int IN_4 = 5;

int EN_A = 3;
int EN_B = 9;

//constant
float Kp = 2.1;

void setup() {
  Wire.begin(0x8);
  Serial.begin(9600);
  Wire.onReceive(receiveEvent);

  pinMode(EN_A , OUTPUT);
  pinMode(EN_B , OUTPUT);
  pinMode(IN_1 , OUTPUT);
  pinMode(IN_2 , OUTPUT);
  pinMode(IN_3 , OUTPUT);
  pinMode(IN_4 , OUTPUT);

}


void receiveEvent(int howMany) {

  while (Wire.available()) {
    byte c = Wire.read();
    Serial.print(int(c));
    Serial.print("\n");
    if (c <= 70)
    {
      float i = Kp * ( 40 + c);
      {
       digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(EN_B , 70);
      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(EN_A , i);
    }
    }
    else if (c >= 110)
    {
      float i = Kp * (200  - c);
     {
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(EN_B , i);
      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(EN_A , 70);
    }
    }
    else if (c > 70 && c < 110)
    {
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(EN_A , 180);
      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(EN_B , 180);
    }




  }

}
void loop()
{
  delay(10);
}
