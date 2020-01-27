#!/usr/bin/env python
#encoding: utf8
import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import LightSensorValues

class LightsensorTest(unittest.TestCase):
	def setUp(self):
		self.count = 0
		rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

	def callback(self.data):
		self.count += 1
		self.values = data
	
	def check_values(self,lf,ls,rs,rf):
		vs = self.values
		self.assertEqual(vs.left_forward, lf, "different value: left_forward")
		self.assertEqual(vs.left_side, ls, "different value: left_side")
		self.assertEqual(vs.right_side, rs, "different value: right_side")
		self.assertEqual(vs.right_forward, rf, "different ralue: right_forward")
		self.assertEqual(vs.sum_all, lf+ls+rs+rf, "different value: sum_all")
		self.assertEqual(vs.sum_forward, lf+rf, "different value:sum_forward")

	def test_node_exist(self):
		nodes = rosnode.get_node_names()
		self.assertIn('/lightsensors',nodes, "node does not exist")

	def test_get_value(self):
		rospy.set_param('lightsensors_freq',10)
		time.sleep(2)
		with open("/dev/rtlightsensor0","w") as f:
			f.write("-1 0 123 432\n")

		time.sleep(3)
			
