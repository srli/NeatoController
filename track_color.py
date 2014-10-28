import cv2
import numpy as np
from cv2 import cv


if __name__ == "__main__":

	cap = cv2.VideoCapture(0)

	cv2.namedWindow("Gaussian Blur")
	cv2.namedWindow("HSV Image")


	while True:
		ret, frame = cap.read()
		cimg = frame

		imgHSV = cv2.cvtColor(cimg, cv.CV_BGR2HSV)
		imgThreshed = cv2.inRange(imgHSV, np.array((60,70,70)), np.array((120,255,255)))

		gaussian_res = cv2.GaussianBlur(imgThreshed, (9,9), 2, 2)

		cv2.imshow("Gaussian Blur", gaussian_res)
		cv2.imshow("HSV Image", imgHSV)
		c = cv2.waitKey(10)