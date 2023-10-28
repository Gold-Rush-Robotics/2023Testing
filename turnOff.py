from grr_roboclaw.roboclaw import Roboclaw
import time


roboclaw = Roboclaw("/dev/ttyS0", 38400, retries=3)
roboclaw.Open()

roboclaw.ForwardM1(129, 0)
roboclaw.ForwardM1(130, 0)
roboclaw.ForwardM2(129, 0)
roboclaw.ForwardM2(130, 0)