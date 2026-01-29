# This launch file is based on
# https://github.com/moveit/moveit_resources/blob/ros2/panda_moveit_config/launch/demo.launch.py

import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, Shutdown
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
import xacro

def load_yaml(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return yaml.safe_load(file)
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None

def load_file(package_name, file_path):
    package_path = get_package_share_directory(package_name)
    absolute_file_path = os.path.join(package_path, file_path)

    try:
        with open(absolute_file_path, "r") as file:
            return file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        return None

def generate_launch_description():
    # Declare command-line arguments
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_ip",
            default_value= "192.168.1.2",
            description="IP address of the robot server (remote).",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_port",
            default_value="8899",
            description="RPC port of the robot server.",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "db",
            default_value="false",
            description="Database flag",
        )
    )

    robot_ip = LaunchConfiguration("robot_ip")
    robot_port = LaunchConfiguration("robot_port")
    db_config = LaunchConfiguration("db")

    joint_names_yaml = {
        "joint_name" : load_yaml(
          "aubo_ros2_jazzy_moveit_config", "config/joint_names.yaml"
        )
    }

    moveit_config = (
        MoveItConfigsBuilder("aubo_ros2_jazzy")
        .robot_description(
            file_path="config/aubo_i5.urdf.xacro"
        )
        .robot_description_semantic(file_path="config/aubo_i5.srdf")
        .planning_scene_monitor(
            publish_robot_description=True, publish_robot_description_semantic=True
        )
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(
           pipelines=["ompl"] 
        )
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .to_moveit_configs()
    )

    # Start the actual move_group node/action server
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_config.to_dict()],
        arguments=["--ros-args", "--log-level", "info"],
    )

    # RViz with MoveIt configuration
    rviz_base = os.path.join(
        get_package_share_directory("aubo_ros2_jazzy_moveit_config"), "rviz"
    )
    rviz_config_file = os.path.join(rviz_base, "moveit.rviz")

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2_moveit",
        output="log",
        arguments=["-d", rviz_config_file],
        parameters=[
          moveit_config.robot_description,
          moveit_config.robot_description_semantic,
          moveit_config.planning_pipelines,
          moveit_config.robot_description_kinematics,
          moveit_config.joint_limits
        ],
    )

    #aubo ros2 tarjectory action
    aubo_trajectory_action_node = Node(
        package="aubo_ros2_trajectory_action",
        executable="aubo_ros2_trajectory_action",
        output="screen",
        parameters=[joint_names_yaml],
    )

    #aubo ros2 driver
    aubo_driver_node = Node(
        package="aubo_ros2_driver",
        executable="aubo_ros2_driver",
        output="screen",
        parameters=[{"robot_ip": robot_ip, "robot_port": robot_port}],
    )

    # Publish TF
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[moveit_config.robot_description],
    )

    # Warehouse mongodb server
    # mongodb_server_node = Node(
    #     package="warehouse_ros_mongo",
    #     executable="mongo_wrapper_ros.py",
    #     parameters=[
    #         {"warehouse_port": 33829},
    #         {"warehouse_host": "localhost"},
    #         {"warehouse_plugin": "warehouse_ros_mongo::MongoDatabaseConnection"},
    #     ],
    #     output="screen",
    #     condition=IfCondition(db_config),
    # )

    nodes = [
        aubo_driver_node,
        aubo_trajectory_action_node,
        move_group_node,
        robot_state_publisher_node,
        rviz_node,
        # mongodb_server_node,
    ]

    return LaunchDescription(declared_arguments + nodes)
