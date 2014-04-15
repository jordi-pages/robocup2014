#! /usr/bin/env python
# vim: expandtab ts=4 sw=4
### FOLLOW_ME.PY ###
import smach
import rospy
"""
@author: Roger Boldu
"""
# Some color codes for prints, from http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
ENDC = '\033[0m'
FAIL = '\033[91m'
OKGREEN = '\033[92m'


from speech_states.say import text_to_say
from speech_states.listen_and_check_word import ListenWordSM
#from speech_states.listen_to import  ListenToSM
#from learn_person import LearnPerson



FOLLOW_GRAMMAR_NAME = 'robocup/followme'

START_FOLLOW_FRASE = "Ok, I'll follow you wherever you want. Please come a bit closer if you are too far, then Please stay still while I learn how you are."
LEARNED_PERSON_FRASE = "Let's go buttercup."
START_FRASE="Hello, my name is REEM! What do you want me to do today?"



# It's only becouse i can't import the file... i can't understand
class LearnPerson(smach.State):

    def __init__(self): 
        smach.State.__init__(self, input_keys=['asr_userSaid'],output_keys=['in_learn_person','asr_userSaid'],
                             outcomes=['succeeded','aborted', 'preempted'])

    def execute(self, userdata):
        userdata.in_learn_person="hello"
        return 'succeeded'


class FollowMeInit(smach.StateMachine):
    def __init__(self):
        smach.StateMachine.__init__(self, ['succeeded', 'preempted', 'aborted'],output_keys=['standard_error','in_learn_person'])

        with self:
            self.userdata.tts_wait_before_speaking=0
            self.userdata.tts_text=None
            self.userdata.tts_lang=None
            self.userdata.standard_error='OK'
            smach.StateMachine.add('INTRO',
                                   text_to_say(START_FRASE),
                                   transitions={'succeeded': 'Listen','aborted':'aborted'})

            smach.StateMachine.add('Listen',
                                   ListenWordSM("follow me"),
                                   transitions={'succeeded': 'START_FOLLOWING_COME_CLOSER',
                                                'aborted': 'Listen'})
          
            smach.StateMachine.add('START_FOLLOWING_COME_CLOSER',
                                   text_to_say(START_FOLLOW_FRASE),
                                   transitions={'succeeded': 'SM_LEARN_PERSON','aborted':'aborted'})

            # it learns the person that we have to follow
            smach.StateMachine.add('SM_LEARN_PERSON',
                                   LearnPerson(),
                                   transitions={'succeeded': 'SM_STOP_LEARNING',
                                                'aborted': 'aborted'})

            smach.StateMachine.add('SM_STOP_LEARNING',
                                   text_to_say(LEARNED_PERSON_FRASE),
                                   transitions={'succeeded': 'succeeded','aborted':'aborted'})
