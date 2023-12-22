#!/usr/bin/env python3
import cv2
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher("poscam_topic", Int16 , queue_size = 10)
    new_pub = rospy.Publisher("statecam_topic", String, queue_size = 10)
    rospy.init_node ("talker", anonymous = True)
    rate = rospy.Rate(1) #freq hz
    state, pos = "yes", 15
    pub.publish(pos)
    new_pub.publish(state)
    rate.sleep()

def open_camera():
    # Open the default camera (usually the first camera, index 0)
    cap = cv2.VideoCapture(1)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        talker()
        return

    # Loop to continuously capture and display frames from the camera
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the captured frame
        cv2.imshow('Camera', frame)
        talker()
        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Call the function to open and display the camera feed
open_camera()
