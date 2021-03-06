#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Cristina De Saint Germain
@email: crsaintc8@gmail.com

12/04/2014

"""

import rospy
import smach
import math

from navigation_states.nav_to_poi import nav_to_poi
from speech_states.say import text_to_say
from object_grasping_states.recognize_object import recognize_object
from object_grasping_states.get_object_information import GetObjectInfoSM

class prepareData(smach.State):
    
    def __init__(self, object_name):
        
        smach.State.__init__(self, outcomes=['succeeded','aborted', 'preempted'], 
                            input_keys=['object_name'], output_keys=['object_name'])
        self.object_name = object_name
        
    def execute(self, userdata):
           
        if not self.object_name and not userdata.object_name:
            rospy.logerr("Object_name isn't set")
            return 'aborted'
        
        #Priority in init
        userdata.object_name = self.object_name if self.object_name else userdata.object_name   
        
        return 'succeeded'               

class SearchObjectSM(smach.StateMachine):
    """
    Executes a SM that search for object. 
    Given the object name, it search which place is the most probably that we can find it. 
    It goes to the place and start the object recognition. It returns the ObjectDetection information. 

    Required parameters:
    No parameters.

    Optional parameters:
    No optional parameters

    Input keys:
        object_name: string with the object's name
    Output keys:
        object_pose: ObjectDetection with the object's information  
        standard_error: String that show what kind of error could be happened
    No io_keys.

    Nothing must be taken into account to use this SM.
    """

    def __init__(self, object_name = None):
        smach.StateMachine.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'],
                    input_keys=['object_name'],
                    output_keys=['standard_error', 'objectd'])

        with self:
        
            smach.StateMachine.add('PrepareData',
               prepareData(object_name),
               transitions={'succeeded':'get_object_info_sm', 'aborted':'aborted'})
            
            # Obtain the location where the object can stay
            smach.StateMachine.add('get_object_info_sm',
                   GetObjectInfoSM(),
                   transitions={'succeeded': 'say_go_to_poi',
                                'aborted': 'aborted',
                                'preempted': 'preempted'})
            
            # say that it goes to the poi
            smach.StateMachine.add(
                'say_go_to_poi',
                text_to_say("I'm going to take the object"),
                transitions={'succeeded': 'go_to_object', 'aborted': 'aborted', 
                'preempted': 'preempted'}) 
            
            # Go to poi where the object can stay
            smach.StateMachine.add(
                'go_to_object',
                nav_to_poi(),
                remapping={"nav_to_poi_name": "object_location"},
                transitions={'succeeded': 'say_start_recognition', 'aborted': 'aborted'})
            
            # Say start recognition
            smach.StateMachine.add(
                'say_start_recognition',
                text_to_say("I'm going to start object recognition"),
                transitions={'succeeded': 'object_detection', 'aborted': 'object_detection', 
                'preempted': 'preempted'}) 
                  
            # Object Detection
            smach.StateMachine.add(
                'object_detection',
                recognize_object(),
                transitions={'succeeded': 'succeeded', 'aborted': 'get_object_info_sm'})


