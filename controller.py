#!/usr/bin/env python  
import roslib
import rospy
from math import *
import random
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
#from sensor_msgs.msg import LaserScan
import cv2
import numpy as np
from cv2 import cv


def calibrate(images):
	i = 0
	avg = []
	gaussian_images = images
	while i < len(gaussian_images):
		im = gaussian_images[i]
		hist = cv2.calcHist([im], [0], None, [256], [0,256])
		print hist[255]
		avg.append(hist[255])
		i+=1
	#print avg
	return avg

def track_color():
	ret, frame = cap.read()
	cimg = frame

	gaussian_images = []

	img_HSV = cv2.cvtColor(cimg, cv.CV_BGR2HSV)
	
	
	red_Threshed = cv2.inRange(img_HSV, np.array((0,50, 50)), np.array((10,170,200)))
	red_gaussian = cv2.GaussianBlur(red_Threshed, (9,9), 2, 2)

	blue_Threshed = cv2.inRange(img_HSV, np.array((100,0,0)), np.array((120,255,255)))
	blue_gaussian = cv2.GaussianBlur(blue_Threshed, (9,9), 2, 2)

	green_Threshed = cv2.inRange(img_HSV, np.array((70,50,50)), np.array((90,255,255)))
	green_gaussian = cv2.GaussianBlur(green_Threshed, (9,9), 2, 2)

	pink_Threshed = cv2.inRange(img_HSV, np.array((165,70, 60)), np.array((180,255,255)))
	pink_gaussian = cv2.GaussianBlur(pink_Threshed, (9,9), 2, 2)

	yellow_Threshed = cv2.inRange(img_HSV, np.array((25,70,70)), np.array((40,255,255)))
	yellow_gaussian = cv2.GaussianBlur(yellow_Threshed, (9,9), 2, 2)

	total_threshed = red_Threshed + blue_Threshed + green_Threshed + pink_Threshed + yellow_Threshed
	total_gaussian = red_gaussian + blue_gaussian + green_gaussian + pink_gaussian + yellow_gaussian

	#cv2.imshow("Gaussian Blur", gaussian_res)
	#cv2.imshow("HSV Image", total_gaussian)
	cv2.imshow("threshed", total_threshed)
	c = cv2.waitKey(1)

	gaussian_images.append(red_gaussian)
	gaussian_images.append(blue_gaussian)
	gaussian_images.append(green_gaussian)
	gaussian_images.append(pink_gaussian)
	gaussian_images.append(yellow_gaussian)

	return gaussian_images

def find_ratios(img):
	circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT,1,200,
	                            param1=200,param2=20,minRadius=0,maxRadius=1000)

	centers = []

	rows, cols = np.shape(img)

	if circles != None:
		for i in circles[0,:]:
		    # draw the outer circle
			cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
		    # draw the center of the circle
			cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
			centers.append((i[0], i[1]))
		cv2.imshow("Gaussian Blur", img)
		c = cv2.waitKey(10)
	
	origin = (rows/2, cols/2)
	dist_from_origin = (centers[0][0] - origin[0], centers[0][1] - origin[1])
	
	return dist_from_origin


def identify_command(thumb, index, middle, ring, pinky):
	"""we can check to see if we can see the finger in our frame, from there decide what our command is going to be
	calculating relative positions is kind of difficult."""
	command = "."
	print thumb, index, middle, ring, pinky;

	if (thumb & ~index & ~middle & ~ring & ~pinky): #only thumb
		command = "done"
	elif (~thumb & index & ~middle & ~ring & ~pinky): #only index
		command = "forward"
	elif (~thumb & index & middle & ~ring & ~pinky): #index + middle
		command = "back"
	elif (~thumb & index & middle & ring & ~pinky): # index, middle, ring (three fingers)
		command = "right"
	elif (~thumb & index & middle & ring & pinky): # index, middle, ring, pinky (four fingers)
		command = "left"
	elif (thumb & index & middle & ring & pinky) == 1: #all five fingers
		command = "stop"
	elif (~thumb & index & ~middle & ~ring & pinky): # index + pinky = metal hand
		command = "metal"

	# if command != ".":
	# 	print command

	return command


def control_robot(command):
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	if command == "back":    
	    msg = Twist (Vector3 (-0.5, 0, 0), Vector3 (0, 0, 0))
	elif command == "forward":
		msg = Twist (Vector3 (0.5, 0, 0), Vector3 (0, 0, 0))
	elif command == "left":
		msg = Twist (Vector3 (0, 0, 0), Vector3 (0, 0, -0.5))
	elif command == "right":
		msg = Twist (Vector3 (0, 0, 0), Vector3 (0, 0, 0.5))
	elif command == "stop":
		msg = Twist (Vector3 (0, 0, 0), Vector3 (0, 0, 0))
	elif command == "metal":
		msg = Twist (Vector3 (0.5, 0, 0), Vector3 (0, 0, random.random()))
	else:
		msg = Twist (Vector3 (0, 0, 0), Vector3 (0, 0, 0))

	pub.publish(msg)




def find_existing(image, average):
	"""finds whether the finger exists or not. Returns true or false"""
	hist = cv2.calcHist([image], [0], None, [256], [0,256])
	#print hist[255], average
	threshold = 30
	if (hist[255] - average) > threshold:
		return 1
	else:
		return 0

if __name__ == "__main__":
	initialize = True
	rospy.init_node('neato_controller', anonymous=True)
	cap = cv2.VideoCapture(0)

	average_values = [200, 200, 200, 200, 200]
	average_averages = []
	i=0
	while not rospy.is_shutdown():

		gaussian_images = track_color()

		thumb 	= 	gaussian_images[0] #red
		index 	= 	gaussian_images[1] #blue
		middle 	= 	gaussian_images[2] #green
		ring 	= 	gaussian_images[3] #pink
		pinky 	= 	gaussian_images[4] #yellow


		if i<20:
			average_averages.append(calibrate(gaussian_images))
		if i==20:
			avg_thumb = 0
			avg_index = 0
			avg_middle = 0
			avg_ring = 0
			avg_pinky = 0
			for average in average_averages:
				avg_thumb += average[0]
				avg_index += average[1]
				avg_middle += average[2]
				avg_ring += average[3]
				avg_pinky += average[4]
			average_values = [avg_thumb/20, avg_index/20, avg_middle/20, avg_ring/20, avg_pinky/20]
				
		#print average_values

		thumb_state = find_existing(thumb, average_values[0])
		index_state = find_existing(index, average_values[1])
		middle_state = find_existing(middle, average_values[2])
		ring_state =  find_existing(ring, average_values[3])
		pinky_state = find_existing(pinky, average_values[4])

		command = identify_command(thumb_state, index_state, middle_state, ring_state, pinky_state)
		print command
		control_robot(command)
		i += 1