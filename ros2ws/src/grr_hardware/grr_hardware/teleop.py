from typing import List
import rclpy
from rclpy.context import Context

from rclpy.node import Node
from rclpy.parameter import Parameter

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, Vector3
from grr_interfaces.msg import Enable

class Teleop(Node):
    def __init__(self) -> None:
        super().__init__("GRR_Teleop")
        self.subscriber = self.create_subscription(Joy, "joy", self.joyCallback, 10)
        self.twistPub = self.create_publisher(Twist, "cmd_vel", 10)
        self.enablePub = self.create_publisher(Enable, "grr_enable", 10)
        
    def joyCallback(self, data:Joy):
        lside = data.axes[0]
        lup = data.axes[1]
        rside = data.axes[3]
        rup = data.axes[4]
        strafe = lside
        forward = lup
        rotate = rside
        if(strafe or forward or rotate):
            self.enablePub.publish(Enable(attachment=5, enable=True))

        twist = Twist(linear=Vector3(x=strafe, y=forward,z=0.0), angular=Vector3(x=0.0, y=0.0, z=rotate))
        self.twistPub.publish(twist)
        
            
        #self.get_logger().info(f"\nforward = {forward : .2f}\nstrafe = {strafe : .2f}\nrotate = {rotate : .2f}")

def main():
    rclpy.init()
    teleop = Teleop()
    rclpy.spin(teleop)
    
    teleop.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()