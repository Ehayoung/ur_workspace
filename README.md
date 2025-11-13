# UR Workspace Meta Repository

A ROS 2 Jazzy meta-repository for the UR10e robot with vision system integration. This repository manages the workspace structure and VCS dependencies for a complete robot control and planning setup.

## Overview

This is the top-level meta-repository that orchestrates the build and deployment of the UR10e robotic arm workspace. It uses VCS (Version Control System) to manage dependencies, allowing for clean separation between the meta-repo configuration and the actual ROS 2 packages.

**Architecture:**
- **Desktop (Ubuntu 24.04):** Control interface, RViz2 visualization, Gazebo simulation, MoveIt2 planning
- **Raspberry Pi 4b:** Camera node, ArUco marker detection, TF transformations
- **UR10e Robot:** Controlled via Universal Robots ROS2 Driver at `10.30.3.100`
- **Camera:** Arducam IMX219 USB (future milestone)

## Quick Start

### Prerequisites
- ROS 2 Jazzy installed
- VCS tool: `pip install vcstool`
- Python 3.10+

### Setup

1. Clone this meta-repository:
   ```bash
   git clone https://github.com/EHayoung/ur_workspace.git
   cd ur_workspace
   ```

2. Import VCS-managed dependencies:
   ```bash
   vcs import src < ur_ws_dsktp.repos
   ```

3. Install system dependencies:
   ```bash
   rosdep install --ignore-src --from-paths src -y
   ```

4. Build the workspace:
   ```bash
   colcon build --symlink-install
   source install/setup.bash
   ```

## Repository Dependencies

This meta-repository imports the following package:

### [ur_workspace_config](https://github.com/EHayoung/ur_workspace_config)
The main ROS 2 package collection containing:
- **ur_workspace_control** - Launch files, controller configurations, and ros2_control setup for robot motion
- **ur_workspace_description** - URDF/Xacro robot model, meshes, and RViz configurations
- **ur_workspace_moveit_config** - MoveIt2 motion planning configurations

## Directory Structure

```
ur_workspace/
├── src/                           # VCS-managed source directory
│   └── ur_workspace_config/       # Imported via ur_ws_dsktp.repos
│       ├── ur_workspace_control/
│       ├── ur_workspace_description/
│       └── ur_workspace_moveit_config/
├── build/                         # Colcon build output
├── install/                       # Colcon install output
├── log/                           # Colcon build logs
├── .venv/                         # Python virtual environment
├── ur_ws_dsktp.repos             # VCS configuration file
└── README.md                      # This file
```

## Development Workflow

### Building
```bash
cd ~/workspaces/ur_workspace
colcon build --symlink-install
source install/setup.bash
```

### Testing with Mock Hardware
```bash
ros2 launch ur_workspace_control start_robot.launch.py \
  use_mock_hardware:=true ur_type:=ur10e
```

### Real Robot Control
```bash
ros2 launch ur_workspace_control start_robot.launch.py \
  use_mock_hardware:=false robot_ip:=10.30.3.100 ur_type:=ur10e
```

**Note:** Real robot control requires the External Control URCap to be active on the robot pendant.

### Motion Planning with MoveIt2
```bash
ros2 launch ur_workspace_moveit_config move_group.launch.py
```

## Network Configuration

All machines use static IP addresses on the `10.30.3.0/24` network with `ROS_DOMAIN_ID=30`:

- **Robot:** `10.30.3.100`
- **Raspberry Pi:** `10.30.3.101`
- **Desktop (this machine):** `10.30.3.102`

## Additional Resources

- **Development plan:** See `src/ur_workspace_config/docs/outline.md`
- **Extended instructions:** Check `src/ur_workspace_config/.vscode/copilot-instructions.md`
- **Active tasks:** Review `src/ur_workspace_config/TODO.md`

## Key Concepts

### VCS Management
The `src/` directory is fully managed by VCS. Do not manually edit it—use `vcs import` and `vcs pull` commands instead. The `.gitignore` excludes this directory from git to keep the meta-repo lightweight.

### Robot Type
All configurations default to **UR10e**. Joint names, TF prefixes, and controller configs use the `ur10e_` prefix throughout.

### Hardware-First Approach
The workspace follows a "hardware-first" methodology:
1. Establish real robot control
2. Validate with mock hardware
3. Add simulation and vision capabilities

## Contributing

To contribute to the UR workspace:
1. Make changes in the relevant package within `src/ur_workspace_config/`
2. Push to the corresponding GitHub repository
3. Update this meta-repo if needed (rare)

## License

See individual package repositories for license information.

## Contact & Support

For issues, questions, or contributions, please refer to the [ur_workspace_config](https://github.com/EHayoung/ur_workspace_config) repository.
