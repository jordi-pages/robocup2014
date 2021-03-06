#! /usr/bin/env python
'''
Created on 15/03/2014

@author: Cristina De Saint Germain

'''

import rospy
import smach


class TimeOut(smach.State):
    """TimeOut State

    Returns succeeded if the specified time has passed. 
    
    Input Keys:
        wait_time: Time we want to wait
    Output Keys:
        standard_error: String thats shows what fails
    
   """

    def __init__(self, wait_time = None):
        
        smach.State.__init__(self, input_keys=['wait_time', 'standard_error'], output_keys=['wait_time','standard_error'], outcomes=['succeeded', 'aborted'])       
        self.time_init = rospy.Time.now()
        self.wait_time = wait_time

    def execute(self, userdata):  
       
        if not self.wait_time and not userdata.wait_time:
            rospy.logerr("Time isn't set")
            return 'aborted'
        
        #Priority in init
        userdata.wait_time = self.wait_time if self.wait_time else userdata.wait_time  
        
        time_now = rospy.Time.now()
        time_check = time_now.secs - self.time_init.secs
        
        if (time_check > userdata.wait_time):
            userdata.standard_error='Time has passed'
            return 'succeeded'
        else:
            userdata.standard_error="Time hasn't passed"
            return 'aborted'