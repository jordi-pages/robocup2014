#! /usr/bin/env python

import roslib; roslib.load_manifest('gpsrSoar')
import rospy
import sys
import smach
import smach_ros
import actionlib
import time
from translator import idx2obj, obj2idx

from smach_ros import ServiceState, SimpleActionState
from std_srvs.srv import Empty
from GenerateGoalScript import world
from speech_states.say import text_to_say
from sm_gpsr_orders import TEST

#TODO: find_person import FindPersonSM
#TODO: complete_grasp_pipeline import CompleteGraspPipelineStateMachine as GraspSM
#TODO: search_object_with_confidence import SearchObjectWithConfidenceStateMachine as SearchObjSM
from navigation_states.nav_to_poi import nav_to_poi #navigation.move_to_room import MoveToRoomStateMachine as MoveToRoomSM
# from pal_smach_utils.navigation.follow_and_stop import FollowAndStop as FollowMeSM
#TODO: learn_face import LearnFaceStateMachine as LearnPersonSM
#from pal_smach_utils.utils.point_at import SMPointInFront as PointAtSM
#TODO: grasping.sm_release import ReleaseObjectStateMachine as ReleaseSM
#TODO: recognize_face import RecognizeFaceStateMachine as RecognizePersonSM
#TODO: introduce_yourself import IntroduceYourselfStateMachine as IntroduceSM
#TODO: sound_action import SpeakActionState <-- listen to

#edit your path in gpsrSoar/src/pathscript.py

'''
SKILLS TODO:

--go_to (poi)
grasp    (object)           --> grasping
bring_to(person)            --> grasping
bring_to_loc(poi)           --> grasping
find_object(object)         --> object detection
fins_person(person)         --> person detection
point_at(poi)               --> to finish, adding point functionality and finishing turn one
--ask_name()
follow(person)              --> follow me
--introduce_me()
learn_person(person)        --> face recognition
recognize_person(person)    --> face recognition

'''

try:
    from pathscript import *
except ImportError:
    print "PATHSCRIPT COULDN'T BE IMPORTED!!"
    print "pathscript.py isn't in your computer. \n please, create it in: \n $roscd gpsrSoar/src/"
    print "then define: \nPATH_TO_SOAR = [PATH to the bin folder in SOAR]\nPATH_TO_STANFORD_PARSER = [PATH to the stanford parser folder]\n\npointing to these packages folders\n\n"

try:
    PATH_TO_SOAR = roslib.packages.get_pkg_dir("gpsr") + "/../soar9.3.2/bin"
    sys.path.append(PATH_TO_SOAR)
    import Python_sml_ClientInterface as sml
except ImportError:
    try:
        from pathscript import *
    except ImportError:
        print "PATHSCRIPT COULDN'T BE IMPORTED!!"
        print "pathscript.py isn't in your computer. \n please, create it in: \n $roscd gpsrSoar/src/"
        print "then define: \nPATH_TO_SOAR = [PATH to the bin folder in SOAR]\nPATH_TO_STANFORD_PARSER = [PATH to the stanford parser folder]\n\npointing to these packages folders\n\n"

    path = PATH_TO_SOAR
    sys.path.append(path)
    import Python_sml_ClientInterface as sml

SOAR_GP_PATH = roslib.packages.get_pkg_dir("gpsrSoar") + "/SOAR/gp2.soar"
if TEST:
    SLEEP_TIME = 0
else:
    SLEEP_TIME = 3
    
class dummy(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['succeeded', 'preempted', 'aborted'])
    def execute(self, userdata):
        return 'succeeded'
        
class speaker(smach.StateMachine): 
    
    
    def __init__(self, text=None):
        #Initialization of the SMACH State machine
        smach.StateMachine.__init__(self,outcomes=['succeeded', 'preempted', 'aborted'])
        
        with self: 
            
            self.userdata.tts_wait_before_speaking=0
            self.userdata.tts_text=None
            self.userdata.tts_lang=None
            
            smach.StateMachine.add(
                'SaySM',
                text_to_say(text),    #uncomment and comment dumy to make the robot anounce what he is going to do
                #dummy(),
                transitions={'succeeded': 'succeeded', 'preempted': 'preempted', 'aborted': 'aborted'})


def call_go_to(loc_name,world):
    '''
    out = aborted
    tries = 0
    while(out==aborted and tries<3):
        if loc_name == 'exit':
            out = call_exit()
        else:
            print "SM : go_to %s" % (loc_name)
            tosay = "I'm going to the "+loc_name
            speak = SpeakActionState(text=tosay)
            speak.execute(ud=None)
            mr = nav_to_poi()
            mr.userdata._data = {'nav_to_poi_name': loc_name.replace(' ', '_')}#{'room_name': loc_name.replace(' ', '_')}
            #mr.userdata.room_name = loc_name
            out = mr.execute()
        tries = tries+1

    return succeeded '''
    
    tosay = "I'm going to the "+str(loc_name)
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_go_to '+ loc_name)
    #############################################################################
    '''sm = nav_to_poi(poi_name = loc_name)
    sm.execute()'''
    #############################################################################
    world.set_current_position(loc_name)
    time.sleep(SLEEP_TIME)  
    return "succeeded" 

def call_guide_to(loc_name,world):
    
    tosay = "Please follow me to the "+str(loc_name)
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_guide_to '+ loc_name)
    #############################################################################
    '''sm = nav_to_poi(poi_name = loc_name)
    sm.execute()'''
    #############################################################################
    print(world.robot.locId)
    world.set_current_position(loc_name)
    print(world.robot.locId)
    time.sleep(SLEEP_TIME)  
    return "succeeded" 

def call_learn_person(pers): #TODO   #Recorda que abans sempre busca una persona que encara no coneix, revisar SOAR
    '''    out = aborted
    tries = 0
    while(out==aborted and tries<3):
        print "SM : learn_person"
        tosay = "I'm going to learn the person in front of me"
        speak = SpeakActionState(text=tosay)
        speak.execute(ud=None)
        
        lp = LearnPersonSM()
        out = lp.execute()
        #PersonName = lp.userdata.out_person_name
        tries = tries+1
    
    #time.sleep(3)
    return succeeded #(out, PersonName)
    '''
    
    tosay = "I'm going to learn the person in front of me, known as " + pers
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_learn_person ' + pers)    
    #############################################################################
    '''
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded"

def call_recognize_person(pers): #TODO  
    '''    out = aborted
    tries = 0
    while(out==aborted and tries<3):
        print "SM : recognize_person" 
        tosay = "I'm going to recognize the person in front of me"
        speak = SpeakActionState(text=tosay)
        speak.execute(ud=None)
        rp = RecognizePersonSM()
        out = rp.execute()
        PersonName = rp.userdata.out_person_name
        tries = tries+1
    
    return succeeded #(out, PersonName)    '''
    
    tosay = "I'm going to recognize " + pers
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_recognize_person ' + pers)
    #############################################################################
    '''
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded" 

def call_point_at(loc_name): #TODO  #to finish, test and include
    '''
    out = aborted
    tries = 0
    while(out==aborted and tries<3):
        print "SM : point_at" 
        tosay = "I'm going to point"
        speak = SpeakActionState(text=tosay)
        speak.execute(ud=None)
        sm =PointAtSM()
        out = sm.execute()
        tries = tries+1

    return succeeded
    '''
#     rpose = get_current_robot_pose()
#     rpose.execute()
    
    tosay = "I'm going to point to " + loc_name
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_point_at ' + loc_name)
    #############################################################################
    
    sm = point_to_poi(loc_name)    #to finish, test and include
    sm.execute()
    
    #############################################################################    
    time.sleep(SLEEP_TIME)
    return "succeeded"

def call_follow(pers): #TODO   
    print pers
    rospy.logwarn("SM : follow-me")
    tosay = "I'm going to follow " + pers
    speak = speaker(tosay)
    speak.execute()
    #############################################################################
    '''
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded"

def call_find_object(object_name): #TODO 
    '''
    out = aborted
    tries = 0
    while(out==aborted and tries<3):
        print "SM : find_object %s" % (object_name)
        tosay = "I'm going to search for "+object_name
        speak = SpeakActionState(text=tosay)    
        speak.execute(ud=None)
        sm = SearchObjSM()
        sm.userdata.object_to_search_for = object_name
        sm.execute()
        for i in range(len(sm.userdata.object_found.object_list)):
            try:
                sm.userdata.object_found.object_list[i].name == object_name
                return succeeded
            except IndexError:
                tries = tries+1



    if (out == aborted):
        tosayn = "Here it should be the " + object_name + " but I can't see it"
        speakn = SpeakActionState(text=tosayn)    
        speakn.execute(ud=None)
    return succeeded
    '''
    
    tosay = "I'm going to search for " + object_name
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_find_object '+object_name)
    #############################################################################
    '''
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded"

def call_grasp(obj): #TODO #adding grasping
    '''
    out = aborted
    tries = 0
    while(out==aborted and tries<5):
        print "SM : grasp %s" % (obj)
        tosay = "I'm going to grasp the " + obj
        speak = SpeakActionState(text=tosay)
        
        speak.execute(ud=None)
        grasp = GraspSM()
        grasp.userdata._data = {'object_to_search_for': obj, 'ask_for_help_key': False}
        out = grasp.execute()
        tries = tries+1

    return succeeded
    '''
    
    tosay = "I'm going to grasp the " + obj
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_grasp '+obj)
    #############################################################################
    '''
    #grasping here
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded"

def call_find_person(person_name): #TODO 
    # print "SM : find_person %s" % (person_name)
    # tosay = "I'm going to search for a person" #+person_name
    # speak = SpeakActionState(text=tosay)
    # speak.execute(ud=None)
#       fp = FindPersonSM()
#       out = fp.execute()
#       #found_person = fp.userdata.closest_person
#       return succeeded

    tosay = "I'm going to search for the person known as " + person_name
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_find_person '+person_name)
    #############################################################################
    '''
    what did you say
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded"

def call_bring_to(person_name): #TODO #Adding realese and reread tosay with some responsible person
    '''
    out = aborted
    tries = 0
    while(out==aborted and tries<3):
        print "SM : bring_to %s" % (person_name)
        tosay = "Take it please"
        speak = SpeakActionState(text=tosay)
        speak.execute(ud=None)
        r = ReleaseSM()
        r.userdata.releasing_position = None;
        out = r.execute()
    
    return succeeded
    #Remember to control the case when person_name == '', given when we are delivering to a place not a person
    '''
    if person_name == '':
        tosay = "I'm leaving this here, sorry but you asked for a person without name"
    else:
        tosay = person_name + "would you mind picking this up when I release it?"
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_bring_to '+person_name)
    #############################################################################
    '''
    #realese here
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded" 

def call_bring_to_loc(location_name): #TODO #Improve toSay, add realese and, may be add some human recognition to avoid throwing stuff to the ground

    if location_name == '':
        tosay = "I'm leaving this here"
    else:
        tosay = "I took this item here as requested. Referee I know you are here, if no one else is going to pick this provably you will want to take it before I throw it to the floor, thanks"
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn('call_bring_to_loc '+location_name)    
    #############################################################################
    '''
    #realese here
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded" 

def call_ask_name(): #TOMAKESURE this is what we need if we even need this
    '''
    print "SM : ask_name" 
    return call_learn_person()
    '''
    tosay = "Excuse me, would you mind telling me your name?"
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn( 'call_ask_name')
    #############################################################################
    '''
    Maybe we should save that the person in front of me is, instead of a random person the one with the identifier asociated to his name
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded"

def call_introduce_me(): #TOASKSAM for a proper introduction
    '''
    out = aborted
    tries = 0
    while(out==aborted and tries<3):
        print "SM : introduce_me" 
        intr = IntroduceSM()
        out = intr.execute()
        tries = tries+1

    return succeeded
    '''
    
    tosay = "Hi, I am reem a robot designed by PAL robotics and prepared by la Salle students to take part in the robocup competition"
    speak = speaker(tosay)
    speak.execute()
    rospy.logwarn( 'call_introduce_me')
    #############################################################################
    '''
    '''
    #############################################################################
    time.sleep(SLEEP_TIME)
    return "succeeded"


def define_prohibitions(): #TODISCOVER WTF IS THIS
    pass

def create_kernel():
    kernel = sml.Kernel.CreateKernelInCurrentThread()
    if not kernel or kernel.HadError():
        print kernel.GetLastErrorDescription()
        exit(1)
    return kernel

def create_agent(kernel, name):
    agent = kernel.CreateAgent("agent")
    if not agent:
        print kernel.GetLastErrorDescription()
        exit(1)
    return agent

def agent_load_productions(agent, path):
    agent.LoadProductions(path)
    if agent.HadError():
        print agent.GetLastErrorDescription()
        exit(1)


def main(world):
    print "******************************\n******************************\nNew goal\n******************************\n******************************\n"
    first_time = time.time()
    kernel = create_kernel()
    agent = create_agent(kernel, "agent")
    agent_load_productions(agent,SOAR_GP_PATH)
    agent.SpawnDebugger()

    # p_cmd = 'learn --on'
    # res = agent.ExecuteCommandLine(p_cmd)
    # res = kernel.ExecuteCommandLine(p_cmd, agent.GetAgentName)
    kernel.CheckForIncomingCommands()
    p_cmd = 'watch --learning 2'
    res = agent.ExecuteCommandLine(p_cmd)
    print str(res)
    

    goal_achieved = False
    while not goal_achieved:
        agent.Commit()  
        agent.RunSelfTilOutput()
        agent.Commands()
        numberCommands = agent.GetNumberCommands()
        print "Numero de comandos recibidos del agente: %s" % (numberCommands)
        i=0
        if numberCommands == 0:
            print 'KABOOOOOOOOOOOOOOOOOOM!!!!!!!!!!!!!!!'
            return 'aborted'
        else:
            while i<numberCommands:
                command = agent.GetCommand(i)
                command_name = command.GetCommandName()
                print "El nombre del commando %d/%d es %s" % (i+1,numberCommands,command_name)

                out = "NULL"
                if command_name == "navigate":
                    loc_to_navigate = command.GetParameterValue("loc")
                    # loc = trad_loc(loc_to_navigate)
                    # print str(loc_to_navigate)
                    loc = idx2obj(int(loc_to_navigate), 'LOCATIONS')
                    print loc
                    if (loc =="NULL"):
                        print "ERROR: la loacalizacion %s no existe" % (loc_to_navigate)
                    
                    out = call_go_to(loc,world)

                elif command_name == "grasp":
                    obj_to_grasp = command.GetParameterValue("obj")
                    # obj = trad_obj(obj_to_grasp)
                    obj = idx2obj(int(obj_to_grasp),'ITEMS')
                    print obj
                    if (obj =="NULL"):
                        print "ERROR: el objeto %s no existe" % (obj_to_grasp)
                    
                    out = call_grasp(obj)

                elif command_name == "deliver": #to Person
                    try:
                        to_pers = command.GetParameterValue("pers")
                        pers = idx2obj(int(to_pers),'PERSONS')
                        print pers
                        if (pers =="NULL"):
                            print "ERROR: la persona %s no existe" % (to_pers)                        
                        out = call_bring_to(pers)
                    except:                     #or to Loc
                        to_loc = command.GetParameterValue("loc")
                        try:
                            loc = idx2obj(int(to_loc),'LOCATIONS')
                            print loc
                            if (loc =="NULL"):
                                print "ERROR: l'objecte %s no existe" % (to_loc)                        
                            out = call_bring_to_loc(loc)
                        except:
                            loc = ''   
                            print loc
                            out = call_bring_to_loc(loc)

                elif command_name == "search-object":
                
                    obj_to_search = command.GetParameterValue("obj")
                    obj = idx2obj(int(obj_to_search), 'ITEMS')
                    print obj
                    if (obj =="NULL"):
                        print "ERROR: el objeto %s no existe" % (obj_to_search)
                    
                    out = call_find_object(obj)
                
                elif command_name == "search-person":
                    pers_to_search = command.GetParameterValue("pers")
                    pers = idx2obj(int(pers_to_search), 'PERSONS')
                    print pers
                    if (pers =="NULL"):
                        print "ERROR: la persona %s no existe" % (pers_to_search)
                    
                    out = call_find_person(pers)
                

                elif command_name == "point-obj":                    
                    to_loc = command.GetParameterValue("loc")
                    loc = idx2obj(int(to_loc),'LOCATIONS')
                    out = call_point_at(loc)
                
                elif command_name == "ask-name":
                    out = call_ask_name()
                
                elif command_name == "follow":          
                    to_pers = command.GetParameterValue("pers")
                    pers = idx2obj(int(to_pers),'PERSONS')
                    out = call_follow(pers)
                
                elif command_name == "introduce-me":
                    out = call_introduce_me()
                
                elif command_name == "memorize-person":
                    to_pers = command.GetParameterValue("pers")
                    pers = idx2obj(int(to_pers),'PERSONS')
                    out = call_learn_person(pers)
                
                elif command_name == "recognize-person":
                    to_pers = command.GetParameterValue("pers")
                    pers = idx2obj(int(to_pers),'PERSONS')
                    out = call_recognize_person(pers)
                    
                elif command_name == "guide":
                    loc_to_navigate = command.GetParameterValue("loc")
                    loc = idx2obj(int(loc_to_navigate), 'LOCATIONS')
                    print loc
                    if (loc =="NULL"):
                        print "ERROR: la loacalizacion %s no existe" % (loc_to_navigate)
                    out = call_guide_to(loc,world)

                elif command_name == "achieved":
                    goal_achieved = True
                    out = "succeeded"
                
                else:
                    print "ERROR: El commando %s no existe" % (command_name)
                    command.AddStatusComplete()


                print "SM return: %s \n\n" % (out) 
                if out=="succeeded": 
                    command.AddStatusComplete()
                
                else:
                    print "gpsrSoar interface: unknown ERROR"
                    exit(1)
                
                i+=1

    command.AddStatusComplete()
    return 'succeeded'


    kernel.DestroyAgent(agent)
    kernel.Shutdown()
    del kernelCommit


if __name__ == "__main__":
    main()
