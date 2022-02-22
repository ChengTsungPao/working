#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>
#include <vector>
#include <tuple>

#include <QMainWindow>
#include <QFileDialog>
#include <QtCharts>

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/features2d.hpp>

#include "ui_mainwindow.h"

//#include "AlgorithmInterface/AlgorithmInterface.h"
#include "AlgorithmInterface/LoadImage.h"
#include "AlgorithmInterface/Canny.h"
#include "AlgorithmInterface/Contour.h"
#include "AlgorithmInterface/Function.h"
#include "AlgorithmInterface/Gradient.h"
#include "AlgorithmInterface/TestResult.h"
#include "AlgorithmInterface/Constant.h"


using namespace std;
using namespace cv;

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE


class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_Image_Load_Button_clicked();
    void on_Find_Canny_Button_clicked();
    void on_Find_Contour_Button_clicked();
    void on_Calculate_Button_clicked();
    void on_Show_Graph_Button_clicked();

private:
    Ui::MainWindow *ui;

    Mat left_image, right_image;
    Mat left_canny_image, right_canny_image;
    Mat left_smooth_image, right_smooth_image;
    vector<Point> left_image_contour, right_image_contour;
    Mat left_contour_image, right_contour_image;

    vector<tuple<double, double>> left_image_Gradient, right_image_Gradient;
    tuple<vector<double>, vector<double>> left_image_result, right_image_result;

    tuple<int, int> left_image_groundTruth, right_image_groundTruth;

public:
    void plot_graph(tuple<vector<double>, vector<double>> image_result, vector<tuple<double, double>> image_Gradient);

};

extern MainWindow* ui_ext;
#endif // MAINWINDOW_H
