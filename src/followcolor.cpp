#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include <iostream>
#include <stdio.h>
#include <typeinfo>
#include <math.h>

using namespace cv;
using namespace std;


void text_onscreen(Mat src){
  string text = "Reference radius is 50px";
  int fontFace = cv::FONT_HERSHEY_PLAIN;
  double fontScale = 1.5;
  int thickness = 1;
  Point textOrg(20, 20);
  putText(src, text, textOrg, fontFace, fontScale, Scalar(0,0,0,255), thickness,8);
}

int main(int argc,char *argv[])
{
    int c, key;
    double pi = 3.1415926535897;    
    Mat src, gray, gaussian_result;
    Mat imgHSV, imgThreshed;
    
    IplImage* color_img;
    CvCapture* cv_cap = cvCaptureFromCAM(0);
    //cvNamedWindow("Circle Detection",0); // create window
    cvNamedWindow("Gaussian Blur",0);
    cvNamedWindow("HSV Image", 0);

    for(;;) {
      color_img = cvQueryFrame(cv_cap); // get frame
      if(color_img != 0){
        src = color_img;

        //Changing color image to HSV for color filtering
        cvtColor(src, imgHSV, CV_BGR2HSV);
        inRange(imgHSV, Scalar(60, 70, 70), Scalar(120, 255, 255), imgPalm);
        inRange(imgHSV, Scalar(60, 70, 70), Scalar(120, 255, 255), imgPalm);

        // Reduce the noise so we avoid false circle detection
        GaussianBlur( imgThreshed, gaussian_result, Size(9, 9), 2, 2 );
             text_onscreen(src); 

        //imshow("Circle Detection", src);
        imshow("Gaussian Blur", gaussian_result);
        imshow("HSV Image", imgHSV);

        c = cvWaitKey(10); // wait 10 ms or for key stroke
        if(c == 27){
            break; // if ESC, break and quit
          }
        }
      }
    /* clean up */
    cvReleaseCapture( &cv_cap );
    cvDestroyWindow("Video");

    return 0;
}