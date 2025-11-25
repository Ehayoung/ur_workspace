import numpy as np
from scipy.spatial.transform import Rotation as R

# Original calibration values
t_orig = np.array([0.068636, -0.002030, -0.064675])
q_orig = np.array([-0.016097, -0.002954, 0.711337, -0.702660])  # [x, y, z, w]

print("="*60)
print("ORIGINAL CALIBRATION")
print("="*60)
print(f"Translation: X={t_orig[0]*1000:.1f}mm, Y={t_orig[1]*1000:.1f}mm, Z={t_orig[2]*1000:.1f}mm")
print()

print("="*60)
print("TARGET (Real Physical Measurement)")
print("="*60)
print("X ≈ 0mm (coplanar with flange)")
print("Y ≈ -50mm (to the side)")
print("Z ≈ 2mm (PCB thickness forward)")
print()

print("="*60)
print("AXIS REMAPPING OPTIONS")
print("="*60)

r_orig = R.from_quat(q_orig)

# We need to find which calibration axis gives us ~2mm
# Calibration: X=68.6mm, Y=-2.0mm, Z=-64.7mm
# Target: X≈0, Y≈-50, Z≈2

# Y_calib = -2.0mm ≈ Z_target (2mm with sign flip)
# X_calib = 68.6mm ≈ Y_target (-50mm, so needs flip and scaling error)
# Z_calib = -64.7mm ≈ X_target (needs to become ~0, but it's large...)

# More options to try
options = [
    {
        "name": "Option E: Y→Z, X→-Y, Z→X",
        "desc": "Y_calib(-2mm)→Z, X_calib(68.6)→-Y(-68.6≈-50), Z_calib(-64.7)→X",
        "t": np.array([-t_orig[2], -t_orig[0], t_orig[1]]),
        "r_adjust": R.from_euler('yz', [-90, 90], degrees=True),
    },
    {
        "name": "Option F: Y→-Z, X→-Y, Z→-X",
        "desc": "Y_calib→-Z, X_calib→-Y, Z_calib→-X",
        "t": np.array([t_orig[2], -t_orig[0], -t_orig[1]]),
        "r_adjust": R.from_euler('yz', [90, 90], degrees=True),
    },
    {
        "name": "Option G: Z→Z, X→-Y, Y→X",
        "desc": "Z_calib(-64.7)→Z, X_calib(68.6)→-Y, Y_calib(-2)→X",
        "t": np.array([-t_orig[1], -t_orig[0], t_orig[2]]),
        "r_adjust": R.from_euler('z', 90, degrees=True),
    },
    {
        "name": "Option H: Y→Z, Z→-Y, X→X",
        "desc": "Y_calib(-2mm)→Z, Z_calib(-64.7mm)→-Y(+64.7≈+50), X_calib(68.6)→X",
        "t": np.array([t_orig[0], t_orig[2], t_orig[1]]),
        "r_adjust": R.from_euler('x', -90, degrees=True),
    },
    {
        "name": "Option I: Y→-Z, Z→-Y, X→-X",
        "desc": "Y_calib(-2mm)→-Z(+2mm), Z_calib(-64.7mm)→-Y(+64.7), X_calib(68.6)→-X",
        "t": np.array([-t_orig[0], t_orig[2], -t_orig[1]]),
        "r_adjust": R.from_euler('xz', [-90, 180], degrees=True),
    },
]

for i, opt in enumerate(options, 5):
    t_new = opt["t"]
    r_new = opt["r_adjust"] * r_orig
    q_new = r_new.as_quat()
    rpy_new = r_new.as_euler('xyz', degrees=True)
    
    print(f"\n{opt['name']}")
    print(f"  {opt['desc']}")
    print(f"  Position: X={t_new[0]*1000:.1f}mm, Y={t_new[1]*1000:.1f}mm, Z={t_new[2]*1000:.1f}mm")
    
    # Check if close to target
    x_match = "✓" if abs(t_new[0]*1000) < 10 else "✗"
    y_match = "✓" if abs(t_new[1]*1000 + 50) < 20 else "✗"
    z_match = "✓" if abs(t_new[2]*1000 - 2) < 10 else "✗"
    print(f"  Target match: X{x_match} Y{y_match} Z{z_match}")
    
    print(f"  Translation: [{t_new[0]:.6f}, {t_new[1]:.6f}, {t_new[2]:.6f}]")
    print(f"  Quaternion: [{q_new[0]:.6f}, {q_new[1]:.6f}, {q_new[2]:.6f}, {q_new[3]:.6f}]")
    print(f"  RPY: [{rpy_new[0]:.1f}, {rpy_new[1]:.1f}, {rpy_new[2]:.1f}]")
    print(f"\n  Test command:")
    print(f"  ros2 run tf2_ros static_transform_publisher \\")
    print(f"    {t_new[0]:.6f} {t_new[1]:.6f} {t_new[2]:.6f} \\")
    print(f"    {q_new[0]:.6f} {q_new[1]:.6f} {q_new[2]:.6f} {q_new[3]:.6f} \\")
    print(f"    ur10e_tool0 camera_v4_{chr(64+i)}")

print("\n" + "="*60)
print("TARGET: X≈0mm, Y≈-50mm, Z≈2mm")
print("="*60)
