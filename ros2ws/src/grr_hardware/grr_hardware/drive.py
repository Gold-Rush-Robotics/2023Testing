from typing import List
import rclpy
import yaml
from rclpy.node import Node
from rclpy.context import Context
from rclpy.parameter import Parameter
from geometry_msgs.msg import Twist
from grr_interfaces.msg import Motor, MotorSet, Enable

import os

class Drive(Node):
    def __init__(self) -> None:
        super().__init__("drive")
        self.subcription = self.create_subscription(Twist, "cmd_vel", self.drive_callback, 10)
        self.motor_publish = self.create_publisher(MotorSet, "grr_motors", 10)
        self.subcription
        with open("/home/grr/2023Testing/ros2ws/install/grr_hardware/share/grr_hardware/hardware_map.yaml", "r") as f:
            self.HWMAP = yaml.safe_load(f.read())
    
    def drive_motors(self, fl:float, fr:float, bl:float, br:float):
        motors = self.HWMAP["motors"]
        front_left = Motor(address=motors["fl"]["address"], m1=motors["fl"]["m1"], speed=fl * (-1 if motors["fl"]["reversed"] else 1))
        front_right = Motor(address=motors["fr"]["address"], m1=motors["fr"]["m1"], speed=fr * (-1 if motors["fr"]["reversed"] else 1))
        back_left = Motor(address=motors["bl"]["address"], m1=motors["bl"]["m1"], speed=bl * (-1 if motors["bl"]["reversed"] else 1))
        back_right = Motor(address=motors["br"]["address"], m1=motors["br"]["m1"], speed=br * (-1 if motors["br"]["reversed"] else 1))
        self.motor_publish.publish(MotorSet(data=[front_left, front_right, back_left, back_right]))
    
    def drive_mecanum(self, forward, strafe, rotate):
        fl = forward + strafe + rotate
        bl = forward - strafe + rotate
        fr = forward - strafe - rotate
        br = forward + strafe - rotate
        motors = [fl, fr, bl, br]
        max_val = max(motors)
        if max_val >= 1:
            motors = [x/max_val for x in motors]
        self.drive_motors(motors[0], motors[1], motors[2], motors[3])
        
    def drive_callback(self, data: Twist):
        forward = data.linear.y
        strafe = data.linear.x
        rotate = data.angular.z
        self.drive_mecanum(forward, strafe, rotate)
        
def main():
    rclpy.init()
    drive = Drive()
    rclpy.spin(drive)
    
    drive.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
