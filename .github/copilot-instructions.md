# Copilot Instructions for UR10e Vision Workspace

## Project Overview

ROS 2 Jazzy workspace for UR10e robot with vision system integration. Built on Universal Robots ROS2 Driver, follows "robot-first" methodology: establish hardware control before simulation, then add vision capabilities.

**Architecture:**
- Desktop (Ubuntu 24.04): Control, RVIZ2, Gazebo, MoveIt2 planning
- Raspberry Pi 4b: Camera node, ArUco detection, TF transformations  
- UR10e Robot: Universal_Robots_ROS2_Driver at `10.30.3.100`
- Camera: Arducam IMX219 USB (future milestone)

## Critical Patterns

### Robot Type: Always UR10e
All defaults must be `ur10e`, never `ur20` or other models. Joint names, TF prefixes, and controller configs use `ur10e_` prefix:
```yaml
# ros2_controllers.yaml pattern
scaled_joint_trajectory_controller:
  ros__parameters:
    joints:
      - ur10e_shoulder_pan_joint
      - ur10e_shoulder_lift_joint
      - ur10e_elbow_joint
      # ...
```

### Network Configuration
Static IPs are mandatory for reliable operation:
- Robot: `10.30.3.100` (default in launch files)
- Raspberry Pi: `10.30.3.101`
- Desktop: `10.30.3.102`
- **ROS_DOMAIN_ID=30** on all devices

### Launch Architecture
The project uses a three-layer launch structure:
1. **`start_robot.launch.py`** - Entry point, delegates to `ur_robot_driver/ur_control.launch.py`
2. **`rsp.launch.py`** - Robot State Publisher with URDF/Xacro processing, injected via `description_launchfile` arg
3. **`ur_control.launch.py`** (from ur_robot_driver) - Hardware interface, ros2_control, controllers

**Key insight:** Always inject custom description via `description_launchfile` parameter instead of modifying upstream driver.

### Mock Hardware First
Always test with `use_mock_hardware:=true` before real robot:
```bash
# Development/testing
ros2 launch ur_workspace_control start_robot.launch.py \
  use_mock_hardware:=true ur_type:=ur10e

# Production (requires External Control URCap active on pendant)
ros2 launch ur_workspace_control start_robot.launch.py \
  use_mock_hardware:=false robot_ip:=10.30.3.100 ur_type:=ur10e
```

### Kinematics Calibration
Two-stage calibration approach:
- **Development:** `config/default_kinematics.yaml` (bundled UR10e defaults)
- **Production:** `config/ur_workspace_calibration.yaml` (extracted from real robot)

Override via launch arg: `kinematics_parameters_file:=/path/to/calibration.yaml`

### URDF/Xacro Structure
The workspace defines a complete workcell, not just a robot:
```xml
<!-- ur_workspace.urdf.xacro - Top level -->
<xacro:ur_workspace_cell parent="world" ur_type="${arg ur_type}">
  <!-- Includes table, monitor, wall, robot_mount -->
</xacro:ur_workspace_cell>

<!-- ur_workspace_macro.xacro - Defines the cell -->
<link name="table"/>        <!-- FZI table mesh -->
<link name="monitor"/>      <!-- Motek monitor mesh -->  
<link name="wall"/>         <!-- Safety barrier -->
<link name="robot_mount"/>  <!-- UR10e mounting point -->
<xacro:ur_robot name="${ur_type}" parent="robot_mount"/>
```

Position: Robot at `(0.845, 0.85, 0)` on table, facing backward (rpy `0 0 π`).

### Controller Configuration
Standard UR controllers are pre-configured in `config/ros2_controllers.yaml`:
- `joint_state_broadcaster` - Publishes joint states
- `scaled_joint_trajectory_controller` - Primary motion interface (respects speed scaling)
- `io_and_status_controller` - GPIO access
- `force_torque_sensor_broadcaster` - Publishes FT data from tool flange
- `forward_velocity_controller`, `forward_position_controller` - Direct control modes

**All controllers use `ur10e_` prefix** for joint names and sensor references.

### MoveIt Integration
MoveIt configuration in `ur_workspace_moveit_config/`:
- **Planning group:** `ur_arm` (chain from `ur10e_base_link` to `ur10e_tool0`)
- **Named state:** `home` position defined in SRDF
- **Collision disabled:** Between workspace fixtures (table/monitor/wall) and robot links
- Launch with: `ros2 launch ur_workspace_moveit_config move_group.launch.py`

## Development Workflow

### Build Process
```bash
cd ~/workspaces/ur_workspace
colcon build --symlink-install
source install/setup.bash
```
Use `--symlink-install` for rapid Python/launch file iteration.

### Python Environment
VS Code auto-activates `.venv/` and sources ROS overlay. Create it:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel pyyaml typeguard
```
Verify: `which python` → should show `.venv/bin/python`

### Package Structure
Three main packages in `src/ur_workspace_config/`:
- **`ur_workspace_description`** - URDF/Xacro, meshes, RViz configs
- **`ur_workspace_control`** - Launch files, controller configs, ros2_control setup
- **`ur_workspace_moveit_config`** - MoveIt planning configs (SRDF, joint limits, kinematics solvers)

### Dependency Management
Core dependencies in package.xml exec_depend:
- `ur_robot_driver`, `ur_client_library`, `ur_controllers` - UR-specific
- `ur_description` - Upstream UR robot models
- `robot_state_publisher`, `controller_manager`, `ros2_control` - Core ROS2 control stack
- `moveit_*` packages for motion planning (only in moveit_config package)

External source deps managed via `ur_ws_dsktp.repos`.

## Vision System (Future Milestones)

When implementing camera integration:
1. **Frame hierarchy:** `world` → `ur10e_base_link` → `ur10e_tool0` → `ur10e_camera_optical_frame` (published by hand-eye static TF)
2. **Static TF:** Hand-eye calibration from `ur10e_tool0` to `camera` (use `multisensor_calibration` apt package for production)
3. **Topic naming:** `/camera/image_raw`, `/aruco/poses`, `/target_object_pose`
4. **Service interface:** `SetCameraMode.srv` for stream vs. capture modes
5. **ArUco detection:** Runs on Raspberry Pi, publishes world-frame poses after TF transform

## Code Generation Rules

1. **Never use `ur20`** - All references must be `ur10e`
2. **Include proper launch argument defaults** - `robot_ip:=10.30.3.100`, `ur_type:=ur10e`
3. **Follow TF prefix convention** - `${ur_type}_` prefix for all robot frames
4. **Test mock hardware first** - Document both mock and real launch commands
5. **Reference correct package paths** - Use `FindPackageShare("ur_workspace_control")` etc.
6. **Maintain xacro parameter flow** - Pass `ur_type`, `kinematics_parameters_file` through full chain
7. **Update controller configs** - Keep joint names synchronized with TF prefix changes
8. **Document IP assumptions** - Clearly state which device each IP refers to

## Common Issues

**Robot not moving:** Check External Control URCap is running on pendant, verify `use_mock_hardware:=false`  
**TF errors:** Ensure `ur_type` matches throughout launch chain, check `tf_prefix` parameter  
**Build failures:** Run `rosdep install --ignore-src --from-paths src -y` before building  
**ROS communication issues:** Verify `ROS_DOMAIN_ID=30` on all machines, check network connectivity

## Reference Files

- Development plan: `src/ur_workspace_config/docs/outline.md`
- Extended AI instructions: `src/ur_workspace_config/.vscode/copilot-instructions.md`
- Network/build guide: `src/ur_workspace_config/README.md`
- Active tasks: `src/ur_workspace_config/TODO.md`
