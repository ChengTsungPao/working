#ifndef FUNCTION_H
#define FUNCTION_H

#endif // FUNCTION_H

#include <algorithm>
#include <vector>
#include <iostream>
#include <QPainter>
#include <math.h>
#include <tuple>
#include <QtAlgorithms>

#include <QJsonObject>
#include <QJsonDocument>
#include <QJsonArray>
#include <QFile>
#include <string>
#include <limits.h>
#include <QFileDialog>
#include <QDebug>

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/features2d.hpp>

using namespace std;
using namespace cv;

void split(std::string const &str, const char delim, std::vector<std::string> &out);
tuple<int, int> readJsonFile(QString path);
double distance(Vec4i position);
double distance(double x1, double y1, double x2, double y2);
double innerProduct(Vec4i position1, Vec4i position2);
double innerProduct(tuple<double, double> position1, tuple<double, double> position2);
double innerProduct(double x1, double y1, double x2, double y2);
tuple<double, double> normalize(double x, double y);
double sumVector(vector<double> arr, int i, int j);
vector<double> splitVector(vector<double> arr, int i, int j);
tuple<int, int> rotatedImage(Mat &image, tuple<int, int> groundTruth, int angle);


