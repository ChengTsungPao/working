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

#include "Function.h"

using namespace std;
using namespace cv;

tuple<Mat, Mat> Image_Load(QString left_image_filename ,QString right_image_filename);
vector<Point> findBestContour(vector<vector<Point>> contours, vector<Vec4i> &bestTwoLines, vector<int> shape);
vector<Point> orderContour(vector<Point> contour, int x, int y);
void drawContour(Mat &drawImage, vector<Point> image_contour);
void Find_Contour_Button(Mat image, Mat &image_smooth, vector<Point> &image_contour, vector<Vec4i> &bestTwoLines, char imageType);
vector<tuple<double, double>> getGradient(Mat image_smooth, vector<Point> contour);
tuple<vector<double>, vector<double>> getAngleMagnitude(vector<tuple<double, double>> image_Gradient);
int findExtremePointByGradient(vector<tuple<double, double>> image_Gradient);
tuple<bool, vector<Vec4i>> HoughLinesPHandler(vector<int> shape, vector<vector<Point>> contours, unsigned int contourIndex);
vector<Point> findMaxLengthContour(vector<vector<Point>> contours);
void drawLines(Mat &drawImage, vector<Vec4i> bestTwoLines);
