#ifndef CANNY_H
#define CANNY_H

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <vector>

#include "AlgorithmInterface/Constant.h"

using namespace std;
using namespace cv;

void Find_Canny(Mat image, Mat &smooth_image, Mat &canny_image, char imageType);

#endif // CANNY_H
