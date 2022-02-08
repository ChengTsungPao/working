# include "Constant.h"


// Parameter

// ROI Setting
const bool ROISWITCH = true;
const Rect_<int> LEFTCROP = Rect(0,0,1080,700);
const Rect_<int> RIGHTCROP = Rect(2000,0,1080,700);

// Remove noise
const int MEDIAN_KERNEL_SIZE = 11;
const int GAUSSIAN_KERNEL_SIZE = 3;

// Edge Detection Canny
const int LOW_THRESHOLD = 80;
const int HIGH_THRESHOLD = 130;

// Find Contour
// HoughLinesP (void HoughLinesPHandler)
const int minLineLength = 10;
const int maxLineGap = 1;

// Find Extreme Point
// Smooth Angle (void findExtremePointByMinMax)
const int windowSize = 20 + 1;
