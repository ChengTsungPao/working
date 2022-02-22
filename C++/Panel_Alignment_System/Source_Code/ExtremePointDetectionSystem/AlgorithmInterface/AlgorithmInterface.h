#ifndef FUNCTION_H
#define FUNCTION_H

#endif // FUNCTION_H

#include <QFileDialog>
#include <QJsonObject>
#include <QJsonDocument>
#include <QJsonArray>
#include <QFile>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <vector>
#include <tuple>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <math.h>
//#include <opencv2/core/mat.hpp>

#include "AlgorithmInterface/LoadImage.h"
#include "AlgorithmInterface/Canny.h"
#include "AlgorithmInterface/Contour.h"
#include "AlgorithmInterface/Function.h"
#include "AlgorithmInterface/Gradient.h"

using namespace std;
using namespace cv;

Point getExtremePoint(string path, char imageType, bool visiable = false);
Point getExtremePoint(Mat image, char imageType, bool visiable = false);
void showImage(Mat image, Mat smooth_image, Mat canny_image, Mat contour_image, Mat result_image);


