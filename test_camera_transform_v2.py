import numpy as np
from scipy.spatial.transform import Rotation as R

# Original calibration
t_orig = np.array([0.068636, -0.002030, -0.064675])
q_orig = np.array([-0.016097, -0.002954, 0.711337, -0.702660])  # [x, y, z, w]

print("="*60)
print("ORIGINAL CALIBRATION")
print("="*60)
print(f"Translation: [{t_orig[0]:.6f}, {t_orig[1]:.6f}, {t_orig[2]:.6f}]")
print(f"Quaternion: [{q_orig[0]:.6f}, {q_orig[1]:.6f}, {q_orig[2]:.6f}, {q_orig[3]:.6f}]")
print()

print("="*60)
print("COORDINATE REMAPPING OPTIONS")
print("="*60)
print("Testing different mappings of calibration frame to ROS tool0 frame")
print()

# The calibration frame might have used different axis conventions
# We need to remap both translation AND rotation consistently

options = [
    {
        "name": "Option 1: X→X, Y→Y, Z→-Z (flip Z)",
        "t": np.array([t_orig[0], t_orig[1], -t_orig[2]]),
        "q": q_orig,
    },
    {
        "name": "Option 2: X→-Z, Y→-Y, Z→X (90° rotation)",
        "t": np.array([-t_orig[2], -t_orig[1], t_orig[0]]),
        "q": q_orig,
    },
    {
        "name": "Option 3: X→Z, Y→-Y, Z→-X",
        "t": np.array([t_orig[2], -t_orig[1], -t_orig[0]]),
        "q": q_orig,
    },
    {
        "name": "Option 4: X→-X, Y→-Y, Z→Z (flip X and Y)",
        "t": np.array([-t_orig[0], -t_orig[1], t_orig[2]]),
        "q": q_orig,
    },
    {
        "name": "Option 5: X→-Z, Y→Y, Z→X",
        "t": np.array([-t_orig[2], t_orig[1], t_orig[0]]),
        "q": q_orig,
    },
    {
        "name": "Option 6: X→Z, Y→Y, Z→-X",
        "t": np.array([t_orig[2], t_orig[1], -t_orig[0]]),
        "q": q_orig,
    },
]

for i, opt in enumerate(options, 1):
    t = opt["t"]
    q = opt["q"]
    
    print(f"\n{opt['name']}")
    print(f"  Translation: [{t[0]:.6f}, {t[1]:.6f}, {t[2]:.6f}]")
    print(f"  Quaternion: [{q[0]:.6f}, {q[1]:.6f}, {q[2]:.6f}, {q[3]:.6f}]")
    print(f"\n  Test command:")
    print(f"  ros2 run tf2_ros static_transform_publisher \\")
    print(f"    {t[0]:.6f} {t[1]:.6f} {t[2]:.6f} \\")
    print(f"    {q[0]:.6f} {q[1]:.6f} {q[2]:.6f} {q[3]:.6f} \\")
    print(f"    ur10e_tool0 camera_remap{i}")

print("\n" + "="*60)
print("EXPECTED IN RVIZ")
print("="*60)
print("The correct frame should show:")
print("  - Camera in FRONT of tool0 (positive X)")
print("  - Camera ABOVE tool0 (positive Z)")
print("  - Small offset to one side (Y ~ 0)")
print("\nReal measurements: ~69mm forward, ~2mm to side, ~65mm up")
