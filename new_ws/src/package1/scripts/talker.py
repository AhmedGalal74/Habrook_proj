#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import String
from main import get_variables

def talker():

    pub = rospy.Publisher("pos_topic", Int16 , queue_size = 10)
    new_pub = rospy.Publisher("state_topic", String, queue_size = 10)
    rospy.init_node ("talker", anonymous=True)
    rate = rospy.Rate(freq) #freq hz
    state, pos = get_variables()
    while not rospy.is_shutdown():

        
        print (state)
        print(pos)
        pub.publish(pos)
        new_pub.publish(state)
        rate.sleep()

if __name__ == '__main__':
    try:
        global freq
        freq = rospy.get_param("freq")
        talker()
    except rospy.ROSInterruptException:
        pass
