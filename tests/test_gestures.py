import math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")
import gesture_mech as g
from hardware_bridge import pose_to_servos, LIMITS

def feats(o):
    lm = g.fake_hand(o, 640, 400, 0, 144, 1280, 720) * np.array([1280, 720])
    return g.hand_features(lm)

def test_demo_sequence_classifies():
    for name, o in g.DEMO_SEQ:
        f, p, _, _ = feats(o)
        got = g.classify(f, p)
        if name == "MANUAL CONTROL":
            assert got in (None,)
        else:
            assert got == name, (name, got)

def test_roll_sign():
    f, p, roll, _ = g.hand_features(g.fake_hand([1]*5, 640, 400, 20, 144, 1280, 720) * np.array([1280, 720]))
    assert abs(roll - 20) < 3

def test_pose_targets_all_states_finite():
    for st in list(g.VERB) + ["IDLE"]:
        P = g.pose_target(st, [0.5]*5, 0, 1.0, 0.5)
        assert all(math.isfinite(v) for v in P.values())

def test_servo_limits_respected():
    wild = {k: 999 for k in ("al", "ar", "el", "er", "kl", "kr")}
    for v, (lo, hi) in zip(pose_to_servos(wild), LIMITS):
        assert lo <= v <= hi
    low = {k: -999 for k in wild}
    for v, (lo, hi) in zip(pose_to_servos(low), LIMITS):
        assert lo <= v <= hi

def test_render_smoke():
    r = g.Robot(); W, H = 640, 360
    for st in ("PUSH-UPS", "RUNNING IMPLEMENTATION", "POWER STANCE"):
        r.mode = st
        r.update(g.pose_target(st, [0.5]*5, 0, 0, 0), W * .4, 0.03)
        r.draw(np.zeros((H, W, 3), np.uint8), np.zeros((H, W, 3), np.uint8), W, H, 0)
        assert "head" in r.pts
