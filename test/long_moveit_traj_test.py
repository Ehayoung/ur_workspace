#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory
import time

NODE_NAME = 'long_trajectory_test'
ACTION_SERVER = '/scaled_joint_trajectory_controller/follow_joint_trajectory'
JOINTS = [
    'ur10e_shoulder_pan_joint',
    'ur10e_shoulder_lift_joint',
    'ur10e_elbow_joint',
    'ur10e_wrist_1_joint',
    'ur10e_wrist_2_joint',
    'ur10e_wrist_3_joint',
]


def main():
    rclpy.init()
    node = rclpy.create_node(NODE_NAME)
    client = ActionClient(node, FollowJointTrajectory, ACTION_SERVER)

    if not client.wait_for_server(timeout_sec=5.0):
        node.get_logger().error(f'Action server {ACTION_SERVER} not available')
        return 1

    # Create a long, smooth trajectory: move each joint through small sinusoidal steps
    points = []
    total_time = 30.0  # seconds
    num_points = 150
    for i in range(1, num_points + 1):
        t = i * (total_time / num_points)
        # small incremental positions (radians): keep within safe range
        pos = [0.2 * (i / num_points) for _ in JOINTS]
        vel = [0.0 for _ in JOINTS]
        pts = JointTrajectoryPoint()
        pts.positions = pos
        pts.velocities = vel
        pts.time_from_start = rclpy.time.Time(sec=int(t)).to_msg()
        points.append(pts)

    traj = JointTrajectory()
    traj.joint_names = JOINTS
    traj.points = points

    goal_msg = FollowJointTrajectory.Goal()
    goal_msg.trajectory = traj

    node.get_logger().info(f'Sending long trajectory with {len(points)} points over {total_time}s')
    send_goal_future = client.send_goal_async(goal_msg)

    rclpy.spin_until_future_complete(node, send_goal_future, timeout_sec=10.0)
    goal_handle = send_goal_future.result()
    if not goal_handle.accepted:
        node.get_logger().error('Goal rejected')
        return 2

    node.get_logger().info('Goal accepted — waiting for result')
    get_result_future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(node, get_result_future, timeout_sec=total_time + 20)

    res = get_result_future.result().result
    status = get_result_future.result().status
    node.get_logger().info(f'Result status: {status}. Error code: {res.error_code if res else "<none>"}')

    node.destroy_node()
    rclpy.shutdown()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
