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



