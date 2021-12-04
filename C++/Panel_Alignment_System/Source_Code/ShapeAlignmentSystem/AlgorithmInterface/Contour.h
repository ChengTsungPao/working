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
#include <Canny_Ben.h>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <math.h>
//#include <opencv2/core/mat.hpp>

using namespace std;
using namespace cv;

tuple<Mat, Mat> Image_Load(QString left_image_filename ,QString right_image_filename);
vector<Point> findBestContour(vector<vector<Point>> contours, vector<int> shape);
vector<Point> orderContour(vector<Point> contour, int x, int y);
void drawContour(Mat &drawImage, vector<Point> image_contour);
void Find_Contour_Button(Mat image, Mat &image_smooth, vector<Point> &image_contour, char imageType);
vector<tuple<double, double>> getGradient(Mat image_smooth, vector<Point> contour);
tuple<vector<double>, vector<double>> getAngleMagnitude(vector<tuple<double, double>> image_Gradient);
int findExtremePoint(vector<tuple<double, double>> image_Gradient);
