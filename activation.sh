#!/bin/bash

if ! command -v mamba &> /dev/null
then
    echo "Mamba not installed, run $ sudo ./one-time-setup.bash"
    exit 1
fi

mamba activate grr_ros_env
source ros2ws/install/setup.sh