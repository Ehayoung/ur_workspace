import numpy as np
from scipy.spatial.transform import Rotation as R

# Original calibration from your non-ROS setup
t_orig = np.array([0.068636, -0.002030, -0.064675])
q_orig = np.array([-0.016097, -0.002954, 0.711337, -0.702660])  # [x, y, z, w]

print("="*60)
print("ORIGINAL TRANSFORM (from non-ROS calibration)")
print("="*60)
print(f"Translation: [{t_orig[0]:.6f}, {t_orig[1]:.6f}, {t_orig[2]:.6f}]")
print(f"Quaternion: [{q_orig[0]:.6f}, {q_orig[1]:.6f}, {q_orig[2]:.6f}, {q_orig[3]:.6f}]")
r_orig = R.from_quat(q_orig)
rpy_orig = r_orig.as_euler('xyz', degrees=True)
print(f"RPY (degrees): [{rpy_orig[0]:.1f}, {rpy_orig[1]:.1f}, {rpy_orig[2]:.1f}]")
print()

# The issue: ROS optical frame convention vs. your calibration convention
# ROS optical frame: X=right, Y=down, Z=forward (camera looking along +Z)
# Your calibration might be in a different convention

print("="*60)
print("TESTING FRAME CONVENTION ADJUSTMENTS")
print("="*60)

# Option 1: Rotate calibration to match ROS optical frame convention
# X->Z, Y->X, Z->Y means rotate -90° around Y, then -90° around X
print("\nOption 1: Camera frame → ROS optical frame")
print("  (Assumes calibration was X=forward, Y=left, Z=up)")
r_cam_to_optical = R.from_euler('yx', [-90, -90], degrees=True)
r_new1 = r_orig * r_cam_to_optical
q_new1 = r_new1.as_quat()
rpy_new1 = r_new1.as_euler('xyz', degrees=True)
print(f"  Translation: [{t_orig[0]:.6f}, {t_orig[1]:.6f}, {t_orig[2]:.6f}]")
print(f"  Quaternion: [{q_new1[0]:.6f}, {q_new1[1]:.6f}, {q_new1[2]:.6f}, {q_new1[3]:.6f}]")
print(f"  RPY (degrees): [{rpy_new1[0]:.1f}, {rpy_new1[1]:.1f}, {rpy_new1[2]:.1f}]")
print(f"\n  Test command:")
print(f"  ros2 run tf2_ros static_transform_publisher \\")
print(f"    {t_orig[0]:.6f} {t_orig[1]:.6f} {t_orig[2]:.6f} \\")
print(f"    {q_new1[0]:.6f} {q_new1[1]:.6f} {q_new1[2]:.6f} {q_new1[3]:.6f} \\")
print(f"    ur10e_tool0 camera_test1")

# Option 2: Different convention (X=forward, Y=down, Z=right)
print("\nOption 2: Different camera convention")
r_cam_to_optical2 = R.from_euler('xy', [-90, 90], degrees=True)
r_new2 = r_orig * r_cam_to_optical2
q_new2 = r_new2.as_quat()
rpy_new2 = r_new2.as_euler('xyz', degrees=True)
print(f"  Translation: [{t_orig[0]:.6f}, {t_orig[1]:.6f}, {t_orig[2]:.6f}]")
print(f"  Quaternion: [{q_new2[0]:.6f}, {q_new2[1]:.6f}, {q_new2[2]:.6f}, {q_new2[3]:.6f}]")
print(f"  RPY (degrees): [{rpy_new2[0]:.1f}, {rpy_new2[1]:.1f}, {rpy_new2[2]:.1f}]")
print(f"\n  Test command:")
print(f"  ros2 run tf2_ros static_transform_publisher \\")
print(f"    {t_orig[0]:.6f} {t_orig[1]:.6f} {t_orig[2]:.6f} \\")
print(f"    {q_new2[0]:.6f} {q_new2[1]:.6f} {q_new2[2]:.6f} {q_new2[3]:.6f} \\")
print(f"    ur10e_tool0 camera_test2")

# Option 3: Simple 180° flip (camera was backwards)
print("\nOption 3: 180° rotation around Z-axis")
r_flip = R.from_euler('z', 180, degrees=True)
r_new3 = r_orig * r_flip
q_new3 = r_new3.as_quat()
rpy_new3 = r_new3.as_euler('xyz', degrees=True)
print(f"  Translation: [{t_orig[0]:.6f}, {t_orig[1]:.6f}, {t_orig[2]:.6f}]")
print(f"  Quaternion: [{q_new3[0]:.6f}, {q_new3[1]:.6f}, {q_new3[2]:.6f}, {q_new3[3]:.6f}]")
print(f"  RPY (degrees): [{rpy_new3[0]:.1f}, {rpy_new3[1]:.1f}, {rpy_new3[2]:.1f}]")
print(f"\n  Test command:")
print(f"  ros2 run tf2_ros static_transform_publisher \\")
print(f"    {t_orig[0]:.6f} {t_orig[1]:.6f} {t_orig[2]:.6f} \\")
print(f"    {q_new3[0]:.6f} {q_new3[1]:.6f} {q_new3[2]:.6f} {q_new3[3]:.6f} \\")
print(f"    ur10e_tool0 camera_test3")

# Option 4: Identity rotation (use translation only, no rotation adjustment)
print("\nOption 4: Identity rotation (calibration rotation ignored)")
q_identity = np.array([0, 0, 0, 1])  # No rotation
print(f"  Translation: [{t_orig[0]:.6f}, {t_orig[1]:.6f}, {t_orig[2]:.6f}]")
print(f"  Quaternion: [{q_identity[0]:.6f}, {q_identity[1]:.6f}, {q_identity[2]:.6f}, {q_identity[3]:.6f}]")
print(f"  RPY (degrees): [0.0, 0.0, 0.0]")
print(f"\n  Test command:")
print(f"  ros2 run tf2_ros static_transform_publisher \\")
print(f"    {t_orig[0]:.6f} {t_orig[1]:.6f} {t_orig[2]:.6f} \\")
print(f"    {q_identity[0]:.6f} {q_identity[1]:.6f} {q_identity[2]:.6f} {q_identity[3]:.6f} \\")
print(f"    ur10e_tool0 camera_test4")

print("\n" + "="*60)
print("NEXT STEPS")
print("="*60)
print("Test each option by running the commands above in a new terminal.")
print("Check RViz TF display to see which camera_testN frame is positioned correctly:")
print("  - In front of flange (positive X from tool0)")
print("  - Above flange (positive Z from tool0)")
print("  - Z-axis pointing away from robot")
