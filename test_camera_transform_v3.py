import numpy as np
from scipy.spatial.transform import Rotation as R

# Original calibration values
t_orig = np.array([0.068636, -0.002030, -0.064675])
q_orig = np.array([-0.016097, -0.002954, 0.711337, -0.702660])  # [x, y, z, w]

print("="*60)
print("DIAGNOSIS")
print("="*60)
print(f"Original calibration translation: [{t_orig[0]:.6f}, {t_orig[1]:.6f}, {t_orig[2]:.6f}]")
print(f"  X: {t_orig[0]*1000:.1f}mm")
print(f"  Y: {t_orig[1]*1000:.1f}mm")
print(f"  Z: {t_orig[2]*1000:.1f}mm")
print()
print("Current (WRONG) in RViz tool0 frame:")
print("  X: ~+50mm, Y: ~0mm, Z: negative")
print("  Pointing: toward -X")
print()
print("Desired (CORRECT) in tool0 frame:")
print("  X: ~0mm, Y: ~-50mm, Z: ~0-5mm")
print("  Pointing: along +Z")
print()

# Analyze the mapping
print("="*60)
print("COORDINATE MAPPING ANALYSIS")
print("="*60)
print("Calibration X (68.6mm) → tool0 X (~50mm in wrong direction)")
print("Calibration Y (-2.0mm) → tool0 Y (~0mm)")
print("Calibration Z (-64.7mm) → tool0 Z (negative)")
print()
print("Desired position is Y=-50mm, so calibration X should map to tool0 Y")
print("This suggests: calib_X → tool0_-Y")
print()

# The correct mapping based on analysis:
# Calibration X (68.6mm) should become tool0 Y (-68.6mm ≈ -50mm with calibration error)
# Calibration Y (-2mm) should become tool0 X (≈0mm) 
# Calibration Z (-64.7mm) should become tool0 Z (positive, so flip sign: +64.7mm)

# But we need Z to be nearly 0, not 64mm. Let's try different mappings:

options = [
    {
        "name": "Option A: X→-Y, Y→X, Z→-Z",
        "desc": "Calibration frame rotated 90° around Z, then Z flipped",
        "t": np.array([-t_orig[1], -t_orig[0], -t_orig[2]]),
        "r_adjust": R.from_euler('z', -90, degrees=True),
    },
    {
        "name": "Option B: X→-Y, Y→Z, Z→X",
        "desc": "Different axis permutation",
        "t": np.array([t_orig[1], -t_orig[2], -t_orig[0]]),
        "r_adjust": R.from_euler('yz', [-90, -90], degrees=True),
    },
    {
        "name": "Option C: X→-Y, Y→-Z, Z→X", 
        "desc": "Another permutation",
        "t": np.array([t_orig[1], t_orig[2], -t_orig[0]]),
        "r_adjust": R.from_euler('yz', [90, -90], degrees=True),
    },
    {
        "name": "Option D: X→-Y, Z→X, Y→Z",
        "desc": "Swap Y and Z, negate X to Y",
        "t": np.array([t_orig[2], -t_orig[0], -t_orig[1]]),
        "r_adjust": R.from_euler('xy', [-90, -90], degrees=True),
    },
]

r_orig = R.from_quat(q_orig)

print("="*60)
print("CORRECTED TRANSFORM OPTIONS")
print("="*60)

for i, opt in enumerate(options, 1):
    t_new = opt["t"]
    r_new = opt["r_adjust"] * r_orig
    q_new = r_new.as_quat()
    
    print(f"\n{opt['name']}")
    print(f"  {opt['desc']}")
    print(f"  Position: X={t_new[0]*1000:.1f}mm, Y={t_new[1]*1000:.1f}mm, Z={t_new[2]*1000:.1f}mm")
    print(f"  Translation: [{t_new[0]:.6f}, {t_new[1]:.6f}, {t_new[2]:.6f}]")
    print(f"  Quaternion: [{q_new[0]:.6f}, {q_new[1]:.6f}, {q_new[2]:.6f}, {q_new[3]:.6f}]")
    print(f"\n  Test command:")
    print(f"  ros2 run tf2_ros static_transform_publisher \\")
    print(f"    {t_new[0]:.6f} {t_new[1]:.6f} {t_new[2]:.6f} \\")
    print(f"    {q_new[0]:.6f} {q_new[1]:.6f} {q_new[2]:.6f} {q_new[3]:.6f} \\")
    print(f"    ur10e_tool0 camera_v3_{chr(64+i)}")

print("\n" + "="*60)
print("TARGET: X≈0mm, Y≈-50mm, Z≈0-5mm, pointing along +Z")
print("="*60)
