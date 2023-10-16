from typing import List
import rclpy
import yaml
from rclpy import Node
from rclpy.context import Context
from rclpy.parameter import Parameter
from geometry_msgs.msg import Twist
from grr_interfaces.msg import Motor, MotorSet, Enable

class drive(Node):
    def __init__(self, node_name: str, *, context: Context = None, cli_args: List[str] = None, namespace: str = None, use_global_arguments: bool = True, enable_rosout: bool = True, start_parameter_services: bool = True, parameter_overrides: List[Parameter] = None, allow_undeclared_parameters: bool = False, automatically_declare_parameters_from_overrides: bool = False) -> None:
        super().__init__(node_name, context=context, cli_args=cli_args, namespace=namespace, use_global_arguments=use_global_arguments, enable_rosout=enable_rosout, start_parameter_services=start_parameter_services, parameter_overrides=parameter_overrides, allow_undeclared_parameters=allow_undeclared_parameters, automatically_declare_parameters_from_overrides=automatically_declare_parameters_from_overrides)
        self.subcription = self.create_subscription(Twist, "cmd_vel", self.drive_callback, 10)
        self.motor_publish = self.create_publisher(MotorSet, "grr_motors", 10)
        self.subcription
        with open("../resource/hardware_map.yaml", "r") as f:
            self.HWMAP = yaml.safe_load(f.read())
    
    def drive_motors(self, fl:float, fr:float, bl:float, br:float):
        motors = self.HWMAP["motors"]
        front_left = Motor(address=motors["fl"]["address"], m1=motors["fl"]["m1"], speed=fl)
        front_right = Motor(address=motors["fr"]["address"], m1=motors["fr"]["m1"], speed=fr)
        back_left = Motor(address=motors["bl"]["address"], m1=motors["bl"]["m1"], speed=bl)
        back_right = Motor(address=motors["br"]["address"], m1=motors["br"]["m1"], speed=br)
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
