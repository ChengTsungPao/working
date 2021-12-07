#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <iostream>
#include <algorithm>
#include <vector>
#include <math.h>
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
#include "AlgorithmInterface/Contour.h"
#include "AlgorithmInterface/Function.h"
#include "AlgorithmInterface/Gradient.h"
#include "AlgorithmInterface/TestResult.h"


using namespace std;
//using namespace cv;

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
    void on_Find_Contour_Button_clicked();
    void on_Calculate_Button_clicked();
    void on_Show_Graph_Button_clicked();

private:
    Ui::MainWindow *ui;
    //variable for graph
    QVector<double> qv_x, qv_y, qv_x2, qv_y2, qv_x3, qv_y3, qv_x4, qv_y4, qv_x5, qv_y5;


public:
    //Draw the graph (using Qcustomplot API)
    void set_data(tuple<vector<double>, vector<double>> image_result, vector<tuple<double, double>> image_Gradient);   //Data Insert fucntion
    void plot_graph(); //Only Draw function


};

extern MainWindow* ui_ext;
#endif // MAINWINDOW_H
