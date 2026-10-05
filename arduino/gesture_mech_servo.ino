// dev/creator=tubakhxn  -- servo receiver for Gesture Mech (Arduino Uno/Nano, 6 servos)
#include <Servo.h>
const int N = 6;
const int PINS[N] = {3, 5, 6, 9, 10, 11};
const int LO[N]   = {5, 5, 10, 10, 5, 5};      // keep in sync with hardware_bridge.py
const int HI[N]   = {170, 170, 150, 150, 80, 80};
const int NEUTRAL[N] = {12, 12, 20, 20, 6, 6};
const unsigned long WATCHDOG_MS = 500;          // no frames -> neutral pose
Servo sv[N];
unsigned long lastFrame = 0;
char buf[64]; byte n = 0;

void apply(const int *a) {
  for (int i = 0; i < N; i++) sv[i].write(constrain(a[i], LO[i], HI[i]));
}
void setup() {
  Serial.begin(115200);
  for (int i = 0; i < N; i++) sv[i].attach(PINS[i]);
  apply(NEUTRAL);
  lastFrame = millis();
}
void parse() {
  if (buf[0] != 'S') return;
  int a[N]; char *p = buf + 1;
  for (int i = 0; i < N; i++) {
    if (*p != ',') return;
    a[i] = atoi(++p);
    while (*p && *p != ',') p++;
  }
  apply(a);
  lastFrame = millis();
}
void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { buf[n] = 0; parse(); n = 0; }
    else if (n < sizeof(buf) - 1) buf[n++] = c;
  }
  if (millis() - lastFrame > WATCHDOG_MS) apply(NEUTRAL);
}
