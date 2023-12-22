#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from std_msgs.msg import Float32
from std_msgs.msg import String
from geometry_msgs.msg import Vector3Stamped

detecting = "bottle"
state = "no image"
pos = 0.0
msg = Vector3Stamped()

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Function to draw line and calculate distances
def draw_distance_lines(img, box, object_name, reference_point=(0, 0)):
    # Draw bounding box
    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
    
    # Calculate organ point (e.g., top-left corner of the bounding box)
    organ_point = (box[0], box[1])
    
    # Draw line between organ point and reference point
    cv2.line(img, reference_point, organ_point, color=(255, 0, 0), thickness=2)
    
    # Calculate vertical and horizontal distances
    vertical_distance = calculate_distance((organ_point[0], reference_point[1]), organ_point)
    horizontal_distance = calculate_distance((reference_point[0], organ_point[1]), organ_point)
    global pos,state 
    pos = horizontal_distance 
    state = "image captured"
    talker()

    # Display text with distances and object name
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    cv2.putText(img, f"Object: {object_name}", (10, 30), font, font_scale, (0, 255, 0), font_thickness)
    cv2.putText(img, f"Vertical: {vertical_distance:.2f}", (10, 60), font, font_scale, (0, 0, 255), font_thickness)
    cv2.putText(img, f"Horizontal: {horizontal_distance:.2f}", (10, 90), font, font_scale, (255, 0, 0), font_thickness)

def get_variables():
    global state,pos
    return state,pos

def talker():
    pub = rospy.Publisher("message_topic", Vector3Stamped , queue_size = 10)
    #new_pub = rospy.Publisher("state_topic", String, queue_size = 10)
    rospy.init_node ("talker", anonymous = True)
    rate = rospy.Rate(100) #freq hz
    #state, pos = get_variables()
    msg.header.frame_id,msg.vector.x = get_variables()
    pub.publish(msg) #pos
    

# Function to process camera input
def Camera():
    classNames = []
    #classFile = '/package1/coco.names'

    with open("/home/gallelio74/Desktop/new_ws/src/package1/scripts/coco.names", 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    #configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    #weightpath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel("/home/gallelio74/Desktop/new_ws/src/package1/scripts/frozen_inference_graph.pb", "/home/gallelio74/Desktop/new_ws/src/package1/scripts/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")

    cam = cv2.VideoCapture(1)

    width = int(cam.get(3))
    height = int(cam.get(4))
    net.setInputSize(width, height)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
   
    talker()    
    while True:
        success, img = cam.read()
        if not success or img is None:
            print("Error: Failed to capture frame")
            break

        img_resized = cv2.resize(img, (width, height))
        classIds, confs, bbox = net.detect(img_resized, confThreshold=0.5)

        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                if detecting == classNames[classId - 1]:
                    object_name = classNames[classId - 1]
                    draw_distance_lines(img, box, object_name)
                else:
                   global state , pos
                   state = "no image"
                   pos = 0
                   #talker()
                   

        fps=cam.get(cv2.CAP_PROP_FPS)
        #print (fps)
        cv2.imshow('let me die', img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

# Call Camera() Function for video from the camera
Camera()