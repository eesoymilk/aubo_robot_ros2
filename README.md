# Aubo Robot ROS2

## Compatibility

| **Supported OS**          | **Supported ROS2 distribution**                         |
|---------------------------|---------------------------------------------------------|
| Ubuntu 24.04              | [Jazzy](https://docs.ros.org/en/jazzy/index.html)       |

|**AUBO ARCS Teachpendant Version**    |**AUBO ARCS Hardware Version**  |**AUBO ARCS SDK Version**  |
|--------------------------------------|--------------------------------|---------------------------|
|0.29.3-rc.6+2a9b2c1                   |1.0.43-rc.5+f2bfa19             |V0.23.1                    |

## Getting Started

This project was developed for ROS2 Jazzy on Ubuntu 24.04. Other versions of Ubuntu and ROS2 may work, but not supported.

1. Install [ROS2 Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

2. Install `colcon` and additional ROS packages:

    ```bash
    sudo apt install -y \
    python3-colcon-common-extensions \
    python3-rosdep2 \
    libeigen3-dev \
    ros-jazzy-xacro \
    ros-jazzy-moveit* \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-rviz2
    ```

3. Setup workspace:

    ```bash
    mkdir -p ~/aubo_ros2_ws/src
    cd ~/aubo_ros2_ws/src
    git clone -b jazzy-arcs https://github.com/XieShaosong/aubo_robot_ros2.git
    cd aubo_robot_ros2/
    ```

4. Install dependencies:

    ```bash
    cd ~/aubo_ros2_ws
    rosdep update
    rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
    ```

5. Build and source the workspace:

    ```bash
    cd ~/aubo_ros2_ws
    source /opt/ros/jazzy/setup.bash
    colcon build --symlink-install
    source install/setup.bash
    ```

**NOTE**: Remember to source the setup file and the workspace whenever a new terminal is opened:

```bash
source /opt/ros/jazzy/setup.bash
source ~/aubo_ros2_ws/install/setup.bash
```

## Usage

### Using MoveIt

You can also run the MoveIt example and use the `MotionPlanning` plugin in RViZ to start planning:

```bash
ros2 launch aubo_ros2_jazzy_moveit_config aubo_moveit.launch.py robot_ip:=[robot ip]
ros2 topic pub --once /aubo_robot/robot_control std_msgs/msg/String 'data: powerOn'
```

Test sim:
```bash
ros2 launch  aubo_ros2_jazzy_moveit_config aubo_moveit_sim.launch.py
```
