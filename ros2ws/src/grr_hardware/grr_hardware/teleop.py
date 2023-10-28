from typing import List
import rclpy
from rclpy.context import Context

from rclpy.node import Node
from rclpy.parameter import Parameter

from sensor_msgs.msg import Joy

class Teleop(Node):
    def __init__(self) -> None:
        super().__init__("GRR_Teleop")
        self.subscriber = self.create_subscription(Joy, "joy", self.joyCallback, 10)
        
    def joyCallback(self, data:Joy):
        self.get_logger().info(data)

def main():
    rclpy.init()
    teleop = Teleop()
    rclpy.spin(teleop)
    
    teleop.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()