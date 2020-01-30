#!/usr/bin/env python
#encoding: utf8
import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import MotorFreqs
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger

class MotorTestN(unittest.TestCase):
	def setUp(self):
		rospy.wait_for_service('/motor_on')
		rospy.wait_for_service('/motor_off')
		on = rospy.ServiceProxy('/motor_on', Trigger)
		ret = on()

	def file_check(self, dev, value, message):
		with open("/dev/" + dev,"r") as f:
			self.assertEqual(f.readline(), str(value)+"\n", message)

	
        def test_put_cmd_vel(self):
                pub = rospy.Publisher('/cmd_vel', Twist)
                m = Twist()
                m.linear.x = 0.1414
                m.angular.z = 1.57
                for i in range(10):
                        pub.publish(m)
                        time.sleep(0.1)
                        print 'test_put_cmd_vel pub.publish(m)'

                self.file_check("rtmotor_raw_l0",200,"wrong left value from cmd_vel")
                self.file_check("rtmotor_raw_r0",600,"wrong right value from cmd_vel")

                time.sleep(1.1)
                self.file_check("rtmotor_raw_r0",0, "don't stop after 1[s]")
                self.file_check("rtmotor_raw_l0",0, "don't stop after 1[s]")


if __name__ == '__main__':
	rospy.init_node('travis_test_motors_cmd_vel')
	rostest.rosrun('pimouse_ros', 'travis_test_motors_cmd_vel', MotorTestN)




	

