from typing import List
import rclpy
from rclpy.context import Context
from rclpy.node import Node
from rclpy.parameter import Parameter

import time
import board
import digitalio


from grr_interfaces.msg import Motor, MotorSet, Enable

class Robot(Node):
    def __init__(self, *, context: Context = None, cli_args: List[str] = None, namespace: str = None, use_global_arguments: bool = True, enable_rosout: bool = True, start_parameter_services: bool = True, parameter_overrides: List[Parameter] = None, allow_undeclared_parameters: bool = False, automatically_declare_parameters_from_overrides: bool = False) -> None:
        super().__init__("roboclaw", context=context, cli_args=cli_args, namespace=namespace, use_global_arguments=use_global_arguments, enable_rosout=enable_rosout, start_parameter_services=start_parameter_services, parameter_overrides=parameter_overrides, allow_undeclared_parameters=allow_undeclared_parameters, automatically_declare_parameters_from_overrides=automatically_declare_parameters_from_overrides)
        self.attachment_enables = [digitalio.DigitalInOut(board.GPIO8), digitalio.DigitalInOut(board.GPIO7), digitalio.DigitalInOut(board.GPIO5), digitalio.DigitalInOut(board.GPIO6), digitalio.DigitalInOut(board.GPIO12), digitalio.DigitalInOut(board.GPIO16), digitalio.DigitalInOut(board.GPIO20)]
        for attachment in self.attachment_enables:
            attachment.direction = digitalio.Direction.OUTPUT
        self.subscription = self.create_subscription(
            MotorSet, 'grr_motors', self.motor_callback, 10
        )
        self.subscription = self.create_subscription(
            Enable, 'grr_enable', self.enable_callback, 10
        )
        self.subscription
        
    def enable_callback(self, data:Enable):
        self.attachment_enables[data.attachment].value = not data.enable
        
    def motor_callback(self, msg: MotorSet):
        for motor in msg.data:
            self.get_logger().info(f"Addy: {motor.address} Motor: {'m1' if motor.m1 else 'm2'} Speed: {motor.speed}")
            
        
def main(args=None):
    rclpy.init(args=args)
    rci = Robot()
    rclpy.spin(rci)
    rci.destroy_node()
    rclpy.shutdown()
    

if __name__ == "__main__":
    main()