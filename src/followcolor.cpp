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

int histograms(Mat inputimg){
  /// Separate the image in 2 places, black, white
  vector<Mat> bw_planes;
  split(inputimg, bw_planes);

  /// Establish the number of bins
  int histSize = 256;

  /// Set the ranges ( for B,W) )
  float range[] = { 0, 256} ;
  const float* histRange = { range };

  bool uniform = true; bool accumulate = false;

  Mat b_hist, w_hist;

  /// Compute the histograms:
  calcHist( &bw_planes[0], 1, 0, Mat(), b_hist, 1, &histSize, &histRange, uniform, accumulate );
  calcHist( &bw_planes[1], 1, 0, Mat(), w_hist, 1, &histSize, &histRange, uniform, accumulate );
  //calcHist( &bgr_planes[2], 1, 0, Mat(), r_hist, 1, &histSize, &histRange, uniform, accumulate );

  // Draw the histograms for B, G and R
  int hist_w = 512; int hist_h = 400;
  int bin_w = cvRound( (double) hist_w/histSize );

  Mat histImage( hist_h, hist_w, CV_8UC3, Scalar( 0,0,0) );

  /// Normalize the result to [ 0, histImage.rows ]
  normalize(b_hist, b_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );
  normalize(w_hist, w_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );
  //normalize(r_hist, r_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );
/*
  /// Draw for each channel
  for( int i = 1; i < histSize; i++ )
  {
      line( histImage, Point( bin_w*(i-1), hist_h - cvRound(b_hist.at<float>(i-1)) ) ,
                       Point( bin_w*(i), hist_h - cvRound(b_hist.at<float>(i)) ),
                       Scalar( 255, 0, 0), 2, 8, 0  );
      line( histImage, Point( bin_w*(i-1), hist_h - cvRound(w_hist.at<float>(i-1)) ) ,
                       Point( bin_w*(i), hist_h - cvRound(w_hist.at<float>(i)) ),
                       Scalar( 0, 255, 0), 2, 8, 0  );
  }

  /// Display
  namedWindow("calcHist Demo", CV_WINDOW_AUTOSIZE );
  imshow("calcHist Demo", histImage );
*/

  return 0;
}


int main(int argc,char *argv[])
{
    int c, key;
    double pi = 3.1415926535897;    
    Mat src, gray, gaussian_result, imgHSV;
    Mat imgPalm, imgThumb, imgIndex;
    Mat GimgPalm, GimgThumb, GimgIndex;

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
        cvtColor(src, gray, CV_BGR2GRAY);
        //imgPalm = imgHSV;
        inRange(imgHSV, Scalar(0, 1, 1), Scalar(255, 255, 255), imgPalm);
        inRange(imgHSV, Scalar(50, 200, 200), Scalar(70, 255, 255), imgThumb);
        inRange(imgHSV, Scalar(60, 70, 70), Scalar(120, 255, 255), imgIndex); //now we have separate mat images for each part we want to track
        

        // Reduce the noise so we avoid false circle detection
        GaussianBlur( imgPalm, GimgPalm, Size(9, 9), 2, 2 );
        GaussianBlur( imgThumb, GimgThumb, Size(9, 9), 2, 2 );
        GaussianBlur( imgIndex, GimgIndex, Size(9, 9), 2, 2 );

        vector<Vec3f> circles;

        // Apply the Hough Transform to find the circles
        HoughCircles(GimgPalm, circles, CV_HOUGH_GRADIENT, 1, 30, 200, 30, 20, 0 );
        HoughCircles(GimgThumb, circles, CV_HOUGH_GRADIENT, 1, 30, 200, 30, 20, 0 );
        HoughCircles(GimgIndex, circles, CV_HOUGH_GRADIENT, 1, 30, 200, 30, 20, 0 );
        
        cout << circles.size() << endl;

        histograms(gray);


       /* if (circles.size() != 0){
            
            // Draw the circles detected
            //for( size_t i = 0; i < circles.size(); i++ )
            for( size_t i = 0; i < circles.size(); i++ ){
                Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
                int radius = cvRound(circles[i][2]);

                //Drawing each circle
                circle( src, center, 3, Scalar(0,255,0), -1, 8, 0 );//center
                circle( src, center, radius, Scalar(0,0,255), 3, 8, 0 );//circumference

                //Drawing lines relative to center
                Point midpoint(center.x, center_screen.y);
                line(src, center_screen, center, Scalar(255,0,0), 1, 8, 0);//center to center
                line(src, center_screen, midpoint, Scalar(255,0,0), 1, 8, 0);//y
                line(src, midpoint, center, Scalar(255,0,0), 1, 8, 0);//x
                
                //cout << "center : " << center << "\nradius : " << radius << endl;
                
                double x_distance = center.x - center_screen.x;
                double y_distance = center.y - center_screen.y;

                double distance = 126.964*exp(-0.0216358 * radius);
                double pan_angle = tan(x_distance/distance);
                double tilt_angle = tan(y_distance/distance);

                printf("");

                key = cvWaitKey(100);

                if(key == 97){
                //angle = fmod(angle, pi);
                printf("Robot Coordinates\n");
                cout << "radius:  " << radius << endl;
                cout << "pan:  " << pan_angle << endl;
                cout << "tilt:  " << tilt_angle << endl;
                cout << "distance:  " << distance << endl;
                cout << "-------------" << endl;
            }
        }
    }*/

        //text_onscreen(src); 

        //imshow("Circle Detection", src);
        imshow("Src", src);
      //  imshow("Gaussian Blur", imgThumb);
        imshow("HSV Image", imgIndex);

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