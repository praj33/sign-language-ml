int f1 = A0;
int f2 = A1;
int f3 = A2;
int f4 = A3;
int f5 = A4;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  Serial.print(analogRead(f1)); Serial.print(",");
  Serial.print(analogRead(f2)); Serial.print(",");
  Serial.print(analogRead(f3)); Serial.print(",");
  Serial.print(analogRead(f4)); Serial.print(",");
  Serial.println(analogRead(f5));

  delay(150);
}