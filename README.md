# Gesture Mech — Agentic AI Robot Control Interface
Dev/Creator: **tubakhxn**

A computer-vision + robotics experiment: hand and finger gestures drive a stylized
on-screen mechanical robot (and, optionally, a real servo rig).

> Educational / research project. By default it controls a **simulated** robot.

## Pipeline
See → Understand → Decide → Act:
Camera → MediaPipe Hand Landmarker (21 landmarks) → features (finger extension, pinch, roll, center)
→ rule-based gesture classifier (4-frame debounce) → robot state → pose smoothing → procedural animation → HUD
→ *(optional)* serial bridge → Arduino/ESP32 servos.

## Gestures
| Gesture | Robot state |
|---|---|
| Fist (all fingers closed) | PUSH-UPS (with rep counter) |
| Index only | RUNNING IMPLEMENTATION |
| Index + middle | DEPLOYING BUILD |
| Index + pinky | MIGRATING MEMORY |
| Index + middle + ring | POWER STANCE |
| Open palm | SCANNING CODEBASE |
| Thumb + pinky out, rest closed | AUTO MODE |
| Thumb–index pinch + middle extended | COMPILING |
| anything else | MANUAL CONTROL (fingers drive the limbs directly) |

With no hand in view the robot falls back to automatic behaviors.

## Install & run
```bash
pip install -r requirements.txt
python gesture_mech.py                 # webcam (model downloads on first run)
python gesture_mech.py --cam 1         # another camera
python gesture_mech.py --demo          # no camera, synthetic hand
python gesture_mech.py --demo --snap demo.png --snap-t 10
```
Keys: **Q/Esc** exit · **H** hand skeleton · **A** auto mode · **S** screenshot · **F** fullscreen.

## Physical robot (optional)
Six servos: L/R shoulder, L/R elbow, L/R knee.
1. Flash `arduino/gesture_mech_servo.ino` (pins 3,5,6,9,10,11; external servo power, common ground).
2. Test without hardware: `python gesture_mech.py --serial dry`
3. Run for real: `python gesture_mech.py --serial COM3` (or `/dev/ttyUSB0`)

Safety layers: angle limits in Python **and** firmware, slew-rate limiting, and a 500 ms
firmware watchdog that returns to a neutral pose if frames stop. These are conveniences,
not a safety system — use a physical e-stop, current limits, and supervision. Do not
connect to safety-critical machinery.

## Tests
```bash
pytest -q tests
```

## Limitations
Heuristic rules, one hand, gestures fixed in code, no LLM planner, simulated robot by default.

## Roadmap
Two-hand input · body pose · custom learned gestures · natural-language commands + LLM planner ·
closed-loop camera feedback · telemetry · exercise counting · physical trainer robot.
