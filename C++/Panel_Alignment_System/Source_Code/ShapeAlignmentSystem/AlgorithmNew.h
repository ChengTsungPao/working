#ifndef ALGORITHMNEW_H
#define ALGORITHMNEW_H

#endif // ALGORITHMNEW_H

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include "mainwindow.h"
using namespace cv;

void drawContour(Mat &drawImage, vector<Point> image_contour);
void Find_Contour_Button(Mat image, Mat &image_smooth, vector<Point> &image_contour, char imageType);
vector<tuple<double, double>> getGradient(Mat image_smooth, vector<Point> contour);
tuple<vector<double>, vector<double>> getAngleMagnitude(vector<tuple<double, double>> image_Gradient);
int findExtremePoint(vector<tuple<double, double>> image_Gradient);
