import os
import xacro
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_bb_bot = get_package_share_directory('bb_bot')
    default_map_path = os.path.join(pkg_bb_bot, 'maps', 'my_map_save.yaml')
    default_xacro_path = os.path.join(pkg_bb_bot, 'description', 'robot.urdf.xacro')  # 你的 xacro 文件路径

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_yaml = LaunchConfiguration('map', default=default_map_path)

    # 先用 xacro 解析器展开
    robot_description_config = xacro.process_file(default_xacro_path)
    robot_description = {'robot_description': robot_description_config.toxml()}

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              description='Use simulation time'),
        DeclareLaunchArgument('map', default_value=default_map_path,
                              description='Full path to map file'),

        # 地图服务器
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'yaml_filename': map_yaml
            }]
        ),

        # robot_state_publisher，传入展开后的 URDF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                **robot_description
            }]
        ),
    ])
