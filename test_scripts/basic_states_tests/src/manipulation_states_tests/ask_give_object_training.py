#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 12:00:00 2013

@author: Chang long Zhu
@email: changlongzj@gmail.com
"""
import rospy
import smach
import smach_ros
import actionlib
import string

from smach_ros import SimpleActionState
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from math import radians, degrees
from manipulation_states.ask_give_object_grasping import ask_give_object_grasping

class PrintUserdataPose(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'aborted', 'preempted'], input_keys=['current_robot_pose'])

    def execute(self, userdata):
        rospy.loginfo('Current Pose : ' + str(userdata.current_robot_pose))

        return 'succeeded'

def main():
    rospy.loginfo('Ask Give Object')
    rospy.init_node('ask_give_object_grasping_Training')
    sm = smach.StateMachine(outcomes=['succeeded', 'preempted', 'aborted'])
    with sm:
        sm.userdata.object_to_grasp = 'Coke'

        smach.StateMachine.add(
            'dummy_state',
            ask_give_object_grasping(),
            transitions={'succeeded': 'succeeded','preempted':'preempted', 'aborted':'aborted'})

    sm.execute()
    rospy.spin()

if __name__=='__main__':
    main()

    
