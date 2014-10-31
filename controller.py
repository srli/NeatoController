#import rospy
#from math import *
#from std_msgs.msg import String
#from geometry_msgs.msg import Twist, Vector3
#from sensor_msgs.msg import LaserScan
import cv2
import numpy as np
from cv2 import cv

def track_color():
	ret, frame = cap.read()
	cimg = frame

	gaussian_images = []

	img_HSV = cv2.cvtColor(cimg, cv.CV_BGR2HSV)
	
	red_Threshed = cv2.inRange(img_HSV, np.array((0,200,180)), np.array((10,255,255)))
	red_gaussian = cv2.GaussianBlur(red_Threshed, (9,9), 2, 2)

	blue_Threshed = cv2.inRange(img_HSV, np.array((60,70,70)), np.array((120,255,255)))
	blue_gaussian = cv2.GaussianBlur(blue_Threshed, (9,9), 2, 2)

	green_Threshed = cv2.inRange(img_HSV, np.array((60,70,70)), np.array((120,255,255)))
	green_gaussian = cv2.GaussianBlur(green_Threshed, (9,9), 2, 2)

	pink_Threshed = cv2.inRange(img_HSV, np.array((60,70,70)), np.array((120,255,255)))
	pink_gaussian = cv2.GaussianBlur(pink_Threshed, (9,9), 2, 2)

	yellow_Threshed = cv2.inRange(img_HSV, np.array((60,70,70)), np.array((120,255,255)))
	yellow_gaussian = cv2.GaussianBlur(yellow_Threshed, (9,9), 2, 2)

	total_threshed = red_Threshed + blue_Threshed + green_Threshed + pink_Threshed + yellow_Threshed
	total_gaussian = red_gaussian + blue_gaussian + green_gaussian + pink_gaussian + yellow_gaussian

	#cv2.imshow("Gaussian Blur", gaussian_res)
	cv2.imshow("HSV Image", img_HSV)
	cv2.imshow("threshed", total_threshed)
	c = cv2.waitKey(1)

	gaussian_images.append(red_gaussian)
	gaussian_images.append(blue_gaussian)
	gaussian_images.append(green_gaussian)
	gaussian_images.append(pink_gaussian)
	gaussian_images.append(yellow_gaussian)

	return gaussian_images

def find_location(img):
	"""
	pass in Image of each finger/plam
	using opencv function, pass out x,y location of point
	"""
	pass





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



def identify_command(thumb_loc, index_loc, middle_loc, ring_loc, pinky_loc):
	pass #something something do stuff with these locations
	return command
	# a = atan2(y,x)
	# dist = squrt(x**2 + y**2)
	# return .2*speed, a

def control_robot(command):
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	if command == "back":    
	    msg = Twist (Vector3 (x, 0, 0), Vector3 (0, 0, a))
	elif command == "forward":
		msg = Twist (Vector3 (x, 0, 0), Vector3 (0, 0, a))
	elif command == "left":
		msg = Twist (Vector3 (x, 0, 0), Vector3 (0, 0, a))
	elif command == "right":
		msg = Twist (Vector3 (x, 0, 0), Vector3 (0, 0, a))



if __name__ == "__main__":
	#rospy.init_node('neato_controller', anonymous=True)
	cap = cv2.VideoCapture(0)

	#cv2.namedWindow("Gaussian Blur")
	cv2.namedWindow("HSV Image")


	while True:
		gaussian_images = track_color()
		thumb 	= 	gaussian_images[0]
		index 	= 	gaussian_images[1]
		middle 	= 	gaussian_images[2]
		ring 	= 	gaussian_images[3]
		pinky 	= 	gaussian_images[4]

		thumb_loc = find_location(thumb)
		index_loc = find_location(index)
		middle_loc = find_location(middle)
		ring_loc = find_location(ring)
		pinky_loc = find_location(pinky)

		command = identify_command(thumb_loc, index_loc, middle_loc, ring_loc, pinky_loc)
		control_robot(command)

		#(x,y) = find_ratios(track_color())
		#control_robot(find_command(x,y))
