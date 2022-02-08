#ifndef CONSTANT_H
#define CONSTANT_H

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
using namespace cv;

/////////////////////////////////////////////////////////////

// Parameter

// ROI Setting
const bool ROISWITCH = true;
const Rect_<int> LEFTCROP = Rect(0, 0, 1080, 700);
const Rect_<int> RIGHTCROP = Rect(200, 0, 1080, 700);

// Remove noise
const int MEDIAN_KERNEL_SIZE = 11;
const int GAUSSIAN_KERNEL_SIZE = 3;

// Edge Detection Canny
const int LOW_THRESHOLD = 80;
const int HIGH_THRESHOLD = 130;

// Find Contour
// HoughLinesP (void HoughLinesPHandler)
const int MINLINELENGTH = 10;
const int MAXLINEGAP = 1;

// Find Extreme Point
// Get Gradient (void getGradient)
const int SOBELSIZE = 11;
// Smooth Angle (void findExtremePointByMin
const int WINDOWSIZE = 20 + 1;


/////////////////////////////////////////////////////////////

#endif // CONSTANT_H
