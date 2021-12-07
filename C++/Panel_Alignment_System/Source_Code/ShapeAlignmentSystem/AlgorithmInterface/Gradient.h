#ifndef GRADIENT_H
#define GRADIENT_H

#endif // GRADIENT_H

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

using namespace std;
using namespace cv;

vector<tuple<double, double>> getGradient(Mat image_smooth, vector<Point> contour);
tuple<vector<double>, vector<double>> getAngleMagnitude(vector<tuple<double, double>> image_Gradient);
int findExtremePoint(vector<tuple<double, double>> image_Gradient);



