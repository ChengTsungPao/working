#ifndef MAINWINDOW_H
#define MAINWINDOW_H


#include <QMainWindow>
#include <QFileDialog>
#include <QTimer>
#include <QtCharts>
#include <QChartView>
#include <QLineSeries>


#include "AlignProcessThread.h"
#include "PLCCom.h"
#include "VirtualPointDetection.h"
#include "AppDoc.h"
#include "communication.h"
#include "wviewgraph.h"
#include "secdialog.h"
#include "Drawgraph.h"
#include "Canny_Ben.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/features2d.hpp>




using namespace std;
//using namespace cv;

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

//class QVBoxLayout;
//class QCustomPlot;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();


signals:
   //void Send1(int data);
    //void Send1(vector<tuple<int, int, float>>);
    void Send1(std::vector<std::tuple<float,int,int>>);


protected:
    void paintEvent(QPaintEvent *e);

private slots:
    void on_pushButton_clicked();
    void on_btnCalibrate_clicked();
    void on_pushButton_2_clicked();
    void on_btnStop_clicked();
    void on_btnStart_clicked();
    void on_pushButton_3_clicked();
    void on_pushButton_4_clicked();
    void on_btn_median_clicked();
    void on_table_Left_cellChanged(int row, int column);
    void on_table_right_cellChanged(int row, int column);
    void on_btnRotation_clicked();
    void on_bRotationUse_stateChanged(int arg1);
    void on_pushButton_5_clicked();
    void on_pushButton_6_clicked();
    void on_pushButton_7_clicked();
    void on_pushButton_8_clicked();
    void on_Image_Load_Button_clicked();
    void on_Find_Contour_Button_clicked();
    void on_Calculate_Button_clicked();
    void on_pushButton_12_clicked();
    void on_Show_Graph_Button_clicked();
    void on_pushButton_14_clicked();
    void on_pushButton_15_clicked();
    void on_pushButton_16_clicked();
    void on_pushButton_17_clicked();
    void on_pushButton_18_clicked();

    //radio button event handler
    void radio_button_left();
    void radio_button_right();

    void on_checkBox_stateChanged(int arg1);

    void on_pushButton_19_clicked();

    void on_pushButton_20_clicked();

private:
    Ui::MainWindow *ui;
    AlignProcessThread *testThread;
    SecDialog *dlg;

    //Calibration
    int count_calpos;
    bool bcal_flag;
    QString return_msg;
    CoorData pc;
    CoorData pc2;
    std::vector<CoorData> cal_pos;

    //variable for graph
    QVector<double> qv_x, qv_y, qv_x2, qv_y2, qv_x3, qv_y3, qv_x4, qv_y4, qv_x5, qv_y5;
    bool bchoose_graph; //graph choose left or right, false : left , true : right




public slots:
    //void PrintToScreen();
    void set_calculatedValues();
    void OnTimerCallbackFunc();
    void OnTimerCallbackFunc_Calibration();
    void readACK(QString str);

public:
    //PLC Communication
    Communication* com;
    bool bThreadStatus;
    QString ControlPLC(Communication *, QString, double *);
    void SetPulse(double*, int, int, int);
    void display_log(QString);
    QString _Pulse2MM(double);
    double _Pix2MM(double pix);
    void insertionSort(int window[]);
    int xGradient(Mat image, int x, int y);
    int yGradient(Mat image, int x, int y);
    void showPopup(); //show the pop-up
    void removeduplpt(std::vector<cv::Point>& vec); //중복 Point제거 위해 사용
    void tokenize(std::string const &str, const char delim, std::vector<std::string> &out);

    //Draw the graph (using Qcustomplot API)
    void set_data(tuple<vector<double>, vector<double>> image_result, vector<tuple<double, double>> image_Gradient);   //Data Insert fucntion
    void plot_graph(); //Only Draw function






};

extern MainWindow* ui_ext;
#endif // MAINWINDOW_H
