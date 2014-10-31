import rospy
from math import *
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
import cv2
import numpy as np
from cv2 import cv

def track_color():
	ret, frame = cap.read()
	cimg = frame

	imgHSV = cv2.cvtColor(cimg, cv.CV_BGR2HSV)
	imgThreshed = cv2.inRange(imgHSV, np.array((60,70,70)), np.array((120,255,255)))

	gaussian_res = cv2.GaussianBlur(imgThreshed, (9,9), 2, 2)

	#cv2.imshow("Gaussian Blur", gaussian_res)
	cv2.imshow("HSV Image", imgHSV)
	c = cv2.waitKey(1)
	return gaussian_res

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
	'''
	num_bright_pixels = 0
	for row in range(rows):
		for col in range(cols):
			brightness = img[row,col]
			if brightness==255:
				num_bright_pixels+=1

	print ratio
	'''
	#hist = cv2.calcHist([img],[0],None,[256],[0,256])
	#print type(hist[255])
	#ratio = float(num_bright_pixels) / float(rows*cols)
	#print hist[255]

def find_command(x,y):
	a = atan2(y,x)
	dist = squrt(x**2 + y**2)
	return .2*speed, a

def control_robot(x,a):
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    msg = Twist (Vector3 (x, 0, 0), Vector3 (0, 0, a))

if __name__ == "__main__":
	#rospy.init_node('neato_controller', anonymous=True)
	cap = cv2.VideoCapture(0)

	cv2.namedWindow("Gaussian Blur")
	cv2.namedWindow("HSV Image")

	while True:
		(x,y) = find_ratios(track_color())
		control_robot(find_command(x,y))
