#!/usr/bin/env python3
# dev/creator=tubakhxn
"""Optional serial bridge: sends smoothed robot pose to an Arduino/ESP32 servo rig.

Protocol (ASCII, 20 Hz max):  S,<s0>,<s1>,<s2>,<s3>,<s4>,<s5>\\n   (servo angles, degrees)
Servos: 0 L-shoulder, 1 R-shoulder, 2 L-elbow, 3 R-elbow, 4 L-knee, 5 R-knee.

Safety: angles are clamped to hardware limits here AND in the firmware, output is
slew-limited, and the firmware drops to neutral if frames stop (watchdog).
This is NOT a safety system -- add a physical e-stop for any real build.
"""
import time

LIMITS = [(5, 170), (5, 170), (10, 150), (10, 150), (5, 80), (5, 80)]
NEUTRAL = [12, 12, 20, 20, 6, 6]
MAX_SLEW = 240.0  # deg/s per servo


def pose_to_servos(p):
    raw = [p["al"], p["ar"], p["el"], p["er"], p["kl"], p["kr"]]
    return [min(hi, max(lo, v)) for v, (lo, hi) in zip(raw, LIMITS)]


class ServoBridge:
    def __init__(self, port, baud=115200, hz=20.0):
        self.dt_min = 1.0 / hz
        self.last_t = 0.0
        self.cur = list(NEUTRAL)
        self.dry = port.lower() == "dry"
        self.ser = None
        if not self.dry:
            try:
                import serial
            except ImportError:
                raise SystemExit("pyserial missing. Run:  pip install pyserial")
            self.ser = serial.Serial(port, baud, timeout=0)
            time.sleep(2.0)  # board resets on open

    def _emit(self, vals):
        line = "S," + ",".join("%d" % round(v) for v in vals) + "\n"
        if self.dry:
            print(line.strip())
        else:
            self.ser.write(line.encode())

    def send(self, pose, live=True):
        now = time.time()
        if now - self.last_t < self.dt_min:
            return
        dt = now - self.last_t if self.last_t else self.dt_min
        self.last_t = now
        tgt = pose_to_servos(pose) if live else list(NEUTRAL)
        step = MAX_SLEW * dt
        self.cur = [c + max(-step, min(step, t - c)) for c, t in zip(self.cur, tgt)]
        self._emit(self.cur)

    def close(self):
        try:
            self._emit(NEUTRAL)
            if self.ser:
                self.ser.close()
        except Exception:
            pass
