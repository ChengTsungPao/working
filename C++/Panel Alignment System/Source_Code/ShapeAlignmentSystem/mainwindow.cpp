#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "AlignProcess.h"
#include "PLCCom.h"
#include "QIODevice"
#include <algorithm>
#include <vector>
#include <iostream>
#include <QPainter>
#include <math.h>
#include <tuple>
#include <QtAlgorithms>
#include <map>
#include <unordered_set> //중복 Point 제거 위해 사용
#include <functional>
#include <Canny_Ben.h>
#include "secdialog.h"
#include <QJsonObject>
#include <QJsonDocument>
#include <QJsonArray>
#include <QFile>
#include <string>
#include <limits.h>
#include <QFileDialog>
#include <QDebug>

#define DIFF_ABS(X,Y) ((X)>(Y)? (X)-(Y) : (Y)-(X))

//QT_CHARTS_USE_NAMESPACE

struct myclass_judge_x_coordinate{
    bool operator() (cv::Point pt1, cv::Point pt2) {return (pt1.x < pt2.x);}
}myobject_x_extern_m;


struct myclass_judge_y_coordinate{
    bool operator() (cv::Point pt1, cv::Point pt2) {return (pt1.y < pt2.y);}
}myobject_y_extern_m;

//중복 Point 제거 위해 사용
bool operator==(const cv::Point& pt1, const cv::Point& pt2)
{
    return ((pt1.x == pt2.x) && (pt1.y == pt2.y));
}

namespace std
{
    template<>
    struct hash<cv::Point> //std hash function overriding
    {
        size_t operator()(cv::Point const& pt) const
        {
            return (size_t)(pt.x*100 + pt.y); //make hash data
        }
    };
}

using namespace std;
//using namespace cv;

MainWindow* ui_ext = NULL;

//Thread Object Create
QThread* thread_Align = new QThread;
QThread* thread_PLC = new QThread;
AlignProcess* worker_Align = new AlignProcess();
PLCComProcess* worker_PLC = new PLCComProcess();
VirtualPointDetection* test = new VirtualPointDetection();
//Drawgraph* dl_new = new Drawgraph();

//Timer Create
shared_ptr<QTimer> m_pTimer;
shared_ptr<QTimer> m_CaliTimer; //Calibration Timer


//************************************************//
//Gradient Based method variable
Mat g_InImg1, g_InImg2, g_InImg1_ROI, g_InImg2_ROI, dst1, dst2;
vector<Point> g_contours_left, g_contours_right;
vector<Point> g_contours_left_back, g_contours_right_back; //최종적으로 찾은 Extreme point에서 FineTune(for round extrem point)
vector<Point> g_contour_left_save, g_contour_right_save; //contour shape compare 변수 (기준데이터)
bool bSavecont; //constour shape 저장 여부 확인변수

//test result mat
Mat g_Left_result, g_Right_result;
vector<vector<Point>> g_L_contours, g_R_contours;
int g_L_index, g_R_index;

QString filename;
QString filename2;



//Left
/************************************************************************/
//Angle, Dev
vector<tuple<float, int, int>> data_Left_ang;
vector<tuple<float, int, int>> data_Left_mag;
vector<tuple<float, int, int>> data_Left_ang_smooth;
vector<tuple<float, int, int>> data_Left_mag_smooth;
//Deviation
vector<tuple<float, int, int>> data_Left_ang_dev;
vector<tuple<float, int, int>> data_Left_mag_dev;

vector<tuple<float, int, int>> Left_gx;
vector<tuple<float, int, int>> Left_gy;
vector<tuple<float, int, int>> Left_gradient;

vector<tuple<float, int, int>> Right_gx;
vector<tuple<float, int, int>> Right_gy;
vector<tuple<float, int, int>> Right_gradient;
/************************************************************************/
//Right
/************************************************************************/
//Angle, Dev
vector<tuple<float, int, int>> data_Right_ang;
vector<tuple<float, int, int>> data_Right_mag;
vector<tuple<float, int, int>> data_Right_ang_smooth;
vector<tuple<float, int, int>> data_Right_mag_smooth;
//Deviation
vector<tuple<float, int, int>> data_Right_ang_dev;
vector<tuple<float, int, int>> data_Right_mag_dev;
/************************************************************************/

/***********************************************************************/
//Sobel operation for angle, magnitude
//Left
Mat L_SobelX_2, L_SobelY_2;

//Right
Mat R_SobelX_2, R_SobelY_2;
/***********************************************************************/


/***********************************************************************/
//Label Data Variable
int L_X_label, L_Y_label, R_X_label, R_Y_label;

/***********************************************************************/




//Select visible contour
bool bCntview = false;

//Histrogram equalization mat (use at the gradeint)
Mat L_hist_mat, R_hist_mat;

//Input Mat variable
Mat img, img2;
Mat img_clone, img2_clone; //최종ExtremePoint Save용

//gradient Mat Copy
Mat L_grad_cpy,R_grad_cpy;

//Roation Test flag
bool bTestRot=false;

//variable
int repaint_test_var=0;
float L_angle[640][480], R_angle[640][480], L_mag[640][480], R_mag[640][480] = {0.0f};
float dst_angle_left[640][480]= {0.0f};
float dst_angle_right[640][480]= {0.0f};
float dst_angle_left_derv[640][480]= {0.0f};
Point ExtremePoint,ExtremePoint2;
vector<vector<Point>> contours_left_new;


//Mat for Houghline Test
Mat TestHough;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->pushButton_2->setVisible(false);
    ui->btn_median->setVisible(false);
    ui->pushButton_4->setVisible(false);
    ui->pushButton_3->setVisible(false);


    ui->pushButton_2->setVisible(false);
    ui->btn_median->setVisible(false);
    ui->pushButton_4->setVisible(false);
    ui->pushButton_3->setVisible(false);
    ui->pushButton_5->setVisible(false);
    ui->groupBox_7->setVisible(false);
    ui->pushButton->setVisible(false);
    ui->pushButton_6->setVisible(false);
    ui->bRotationUse->setVisible(false);
    ui->edttestangle->setVisible(false);
    ui->btnRotation->setVisible(false);
    ui->pushButton_18->setVisible(false);
    ui->label_17->setVisible(false);
    ui->label_16->setVisible(false);
    ui->label_18->setVisible(false);
    ui->pushButton_8->setVisible(false);
    ui->pushButton_7->setVisible(false);

    ui->pushButton_17->setVisible(false);
    ui->pushButton_12->setVisible(false);
    ui->pushButton_16->setVisible(false);
    ui->pushButton_14->setVisible(false);
    ui->pushButton_15->setVisible(false);

    ui_ext = this;
    bThreadStatus = false;
    bchoose_graph = false;
    bSavecont = false;

    //#1 graph screen
    //graph1 gx blue
    ui->widget->addGraph();
    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);
    ui->widget->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
    //graph2 gy Red
    ui->widget->addGraph();
    ui->widget->graph(1)->setLineStyle(QCPGraph::lsLine);
    ui->widget->graph(1)->setPen(QPen(QColor(255, 0, 0), 2));

    ui->widget->xAxis->setLabel("Index");
    if(bchoose_graph)
    {
        ui->widget->yAxis->setLabel("Gx,Gy[Right]]");
    }
    else
    {
        ui->widget->yAxis->setLabel("Gx,Gy[Left]]]");
    }

    ui->widget->xAxis->rescale(false);
    ui->widget->yAxis->rescale(false);



    //#2 graph screen
    //graph1 angle blue
    ui->widget_2->addGraph();
    ui->widget_2->graph(0)->setLineStyle(QCPGraph::lsLine);
    ui->widget_2->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
    ui->widget_2->xAxis->setLabel("Index");
    //ui->widget_2->yAxis->setLabel("Angle[Left]");
    if(bchoose_graph)
    {
        ui->widget_2->yAxis->setLabel("Angle[Right]");
    }
    else
    {
        ui->widget_2->yAxis->setLabel("Angle[Left]");
    }
    ui->widget_2->xAxis->rescale(false);
    ui->widget_2->yAxis->rescale(false);
    //ui->widget_2->replot();

    //#3 graph screen
    //graph1 gx blue
    ui->widget_3->addGraph();
    ui->widget_3->graph(0)->setLineStyle(QCPGraph::lsLine);
    ui->widget_3->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
    ui->widget_3->xAxis->setLabel("Index");
    //ui->widget_3->yAxis->setLabel("Magnitude[Left]");
    if(bchoose_graph)
    {
        ui->widget_3->yAxis->setLabel("Magnitude[Right]]");
    }
    else
    {
        ui->widget_3->yAxis->setLabel("Magnitude[Left]");
    }
    ui->widget_3->xAxis->rescale(false);
    ui->widget_3->yAxis->rescale(false);


    connect(ui->radioButton, SIGNAL(clicked()), this, SLOT(radio_button_left()));
    connect(ui->radioButton_2, SIGNAL(clicked()), this, SLOT(radio_button_right()));






}

MainWindow::~MainWindow()
{
    delete ui;
}


bool compare(const tuple<int, int, float>& a, const tuple<int, int, float>& b){
    return (get<2>(a) > get<2>(b));
}

//Data Insert fucntion
void MainWindow::add_data()
{
    if(bchoose_graph) //right image graph
    {
        for(int i=0; i<Right_gx.size(); i++)
        {
            qv_x.append(i);
            qv_y.append(std::get<0>(Right_gx.at(i)));

            qv_x2.append(i);
            qv_y2.append(std::get<0>(Right_gy.at(i)));
        }

        for(int i=0; i<data_Right_ang.size(); i++)
        {
            qv_x3.append(i);
            qv_y3.append(std::get<0>(data_Right_ang.at(i)));
        }
        for(int i=0; i<data_Right_mag.size(); i++)
        {
            qv_x4.append(i);
            qv_y4.append(std::get<0>(data_Right_mag.at(i)));
        }
    }
    else //left image graph
    {
        for(int i=0; i<Left_gx.size(); i++)
        {
            qv_x.append(i);
            qv_y.append(std::get<0>(Left_gx.at(i)));

            qv_x2.append(i);
            qv_y2.append(std::get<0>(Left_gy.at(i)));
        }

        for(int i=0; i<data_Left_ang.size(); i++)
        {
            qv_x3.append(i);
            qv_y3.append(std::get<0>(data_Left_ang.at(i)));
        }
        for(int i=0; i<data_Left_mag.size(); i++)
        {
            qv_x4.append(i);
            qv_y4.append(std::get<0>(data_Left_mag.at(i)));
        }
    }

}

//Only Draw function
void MainWindow::plot_graph()
{
    //Just Draw data of add_data function
    ui->widget->graph(0)->setData(qv_x,qv_y);
    ui->widget->graph(1)->setData(qv_x2,qv_y2);
    ui->widget->rescaleAxes();
    ui->widget->replot();
    ui->widget->update();

    ui->widget_2->graph(0)->setData(qv_x3,qv_y3);
    ui->widget_2->rescaleAxes();
    ui->widget_2->replot();
    ui->widget_2->update();

    ui->widget_3->graph(0)->setData(qv_x4,qv_y4);
    ui->widget_3->rescaleAxes();
    ui->widget_3->replot();
    ui->widget_3->update();

}


void MainWindow::on_pushButton_clicked()
{

    if(bTestRot == false)
    {
        QString filename = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
        QString filename2 = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
        img = cv::imread(filename.toStdString());
        img2 = cv::imread(filename2.toStdString());

    }

    img_clone = img.clone();

    Mat gray, result_el;
    Mat gray2, result_el2;
    Mat img_blur1, img_blur2;


    //Image Load and noise remove
    /*****************************************************/
    //기본전처리
    cv::GaussianBlur(img,img,Size(7,7),2,2);
    cv::cvtColor(img,gray,CV_BGR2GRAY);
    cv::threshold(gray,gray,45,255,THRESH_BINARY);
    //cv::threshold(gray,gray,45,255,THRESH_BINARY | THRESH_OTSU);
    //cv::imshow("Basic",gray);



    //모폴로지
    Mat transM;
    Mat k = cv::getStructuringElement(MORPH_RECT,Size(11,11),Point(-1,-1));
    cv::morphologyEx( gray, transM, MORPH_CLOSE, k, Point(-1,-1),2);                //왼쪽 상부 큰구멍을 매꾸기위한 closing작업


    //sobel operator
    int gx,gy,sum;
    Mat test = Mat::zeros(transM.rows, transM.cols, CV_8UC1);
    for(int y = 1; y < transM.rows - 1; y++)
    {
       for(int x = 1; x < transM.cols - 1; x++)
       {
            //if(y<=1) continue;
            //if(x>=639) continue;
            gx = xGradient(transM, x, y);
            gy = yGradient(transM, x, y);
            sum = abs(gx) + abs(gy);
            sum = sum > 255 ? 255:sum;
            sum = sum < 0 ? 0 : sum;
            test.at<uchar>(y,x) = sum;
        }
     }
     //Median blur
     cv::medianBlur(test,test,3);
     //cv::imshow("Median",test);

    //find contours
    Mat newCanvas = Mat::zeros(transM.rows, transM.cols, CV_8UC1);;
    vector<vector<Point>> contours_left,contours_left_dp, contours_right;
    vector<Vec4i> hierarchy1,hierarchy2;
    findContours( test, contours_left, hierarchy1, RETR_TREE, CHAIN_APPROX_NONE );
    cv::drawContours(img,contours_left,0,Scalar(0,0,255),2,LINE_AA,hierarchy1);              //contour 결과에는 좌표값(x,y)가 저장된다.


    cv::drawContours(newCanvas,contours_left,0,Scalar(255,255,255),2,LINE_AA,hierarchy1);              //contour 결과에는 좌표값(x,y)가 저장된다.
    //cv::imshow("contours_left",newCanvas);


    vector<vector<Point>> hull(contours_left.size());
    convexHull(contours_left[0],hull[0],false);

    //Make a vector for new line
    vector<Point> new_hull;
    for(int i=0; i<hull[0].size()-1; i++)
    {
        new_hull.push_back(hull[0][i]);
    }


    //Make a new line
    vector<vector<Point>> contours_left_new;
    Mat new_hull_img = Mat::zeros(transM.rows, transM.cols, CV_8UC1);
    cv::polylines(new_hull_img, new_hull, false, Scalar(255,255,255), 1, LINE_AA); //Antialising을 위해서 , LINE_AA로 그림!
    //cv::imshow("new_hull_lines",new_hull_img);
    TestHough = new_hull_img.clone();



    findContours( new_hull_img, contours_left_new, hierarchy1, RETR_TREE, CHAIN_APPROX_NONE );
    cv::drawContours(img,contours_left_new,0,Scalar(0,255,0),2,LINE_AA,hierarchy1);


    //contour points data
    //cout << "contour points size: " << contours_left_new[0].size() << endl;
    vector<Point> sorted_contour; //y기준 sort data
    vector<Point> sorted_contour2; //x기준 sort data


    //Hough Line Test

     //insert contour points data(Point) to vector containor
     for(int i=0; i<contours_left_new[0].size(); i++)
     {
         sorted_contour.push_back(contours_left_new[0][i]);
         sorted_contour2.push_back(contours_left_new[0][i]);
     }

     //sort
     // by y
     std::sort(sorted_contour.begin(), sorted_contour.end(), myobject_y_extern_m);
     // by x
     std::sort(sorted_contour2.begin(), sorted_contour2.end(), myobject_x_extern_m);




     //3. Test Print
     //cout << "sorted contour size: " << sorted_contour2.size() << endl;
     /*
     for(int i=0; i<sorted_contour.size(); i++)
     {
        cout <<i<<"Point, X: " << sorted_contour2[i].x <<", Y: "<<sorted_contour2[i].y << endl;
     }
     */

     //4. sampling 7 point  (separte two part)

     int x_s = (sorted_contour.begin())->x;
     int y_s = (sorted_contour.begin())->y;
     int x_s30 = (sorted_contour.begin() + 30)->x;
     int y_s30 = (sorted_contour.begin() + 30)->y;
     int x_s50 = (sorted_contour.begin() + 50)->x;
     int y_s50 = (sorted_contour.begin() + 50)->y;
     int x_s80 = (sorted_contour.begin() + 80)->x;
     int y_s80 = (sorted_contour.begin() + 80)->y;
     int x_s100 = (sorted_contour.begin() + 100)->x;
     int y_s100 = (sorted_contour.begin() + 100)->y;
     int x_s150 = (sorted_contour.begin() + 150)->x;
     int y_s150 = (sorted_contour.begin() + 150)->y;
     int x_s200 = (sorted_contour.begin() + 200)->x;
     int y_s200 = (sorted_contour.begin() + 200)->y;
     int x_s500 = (sorted_contour.begin() + 500)->x;
     int y_s500 = (sorted_contour.begin() + 500)->y;
     int x_s1000 = (sorted_contour.begin() + 1000)->x;
     int y_s1000 = (sorted_contour.begin() + 1000)->y;

     //끝점 x 계산
     int cal_x = (x_s + x_s30 + x_s50 + x_s80 + x_s100 + x_s150 + x_s200)/7;
     int cal_y = (y_s + y_s30 + y_s50 + y_s80 + y_s100 + y_s150 + y_s200)/7;

     Point LINE1_P1(x_s,y_s);
     Point LINE1_P2(cal_x, cal_y);





     //4. sampling 7 point  (separte two part)

     int x_s_2 = (sorted_contour2.end() - 1)->x;
     int y_s_2 = (sorted_contour2.end() - 1)->y;
     int x_s30_2 = (sorted_contour2.end() - 31)->x;
     int y_s30_2 = (sorted_contour2.end() - 31)->y;
     int x_s50_2 = (sorted_contour2.end() - 51)->x;
     int y_s50_2 = (sorted_contour2.end() - 51)->y;
     int x_s80_2 = (sorted_contour2.end() - 81)->x;
     int y_s80_2 = (sorted_contour2.end() - 81)->y;
     int x_s100_2 = (sorted_contour2.end() - 101)->x;
     int y_s100_2 = (sorted_contour2.end() - 101)->y;
     int x_s150_2 = (sorted_contour2.end() - 151)->x;
     int y_s150_2 = (sorted_contour2.end() - 151)->y;
     int x_s200_2 = (sorted_contour2.end() - 201)->x;
     int y_s200_2 = (sorted_contour2.end() - 201)->y;
     int x_s500_2 = (sorted_contour2.end() - 501)->x;
     int y_s500_2 = (sorted_contour2.end() - 501)->y;

     int x_s700_2 = (sorted_contour2.end() - 701)->x;
     int y_s700_2 = (sorted_contour2.end() - 701)->y;

     int x_s900_2 = (sorted_contour2.end() - 901)->x;
     int y_s900_2 = (sorted_contour2.end() - 901)->y;
     int x_s1500_2 = (sorted_contour2.end() - 1501)->x;
     int y_s1500_2 = (sorted_contour2.end() - 1501)->y;


     //cout <<"x : "<<x_s_2<<", y : "<<y_s_2<<"x_end : "<<x_s700_2<<",y_end :"<<y_s700_2<<endl;

     //end - 50번째 Point
     int cal_x_2 = (x_s_2 /*+ x_s30_2 + x_s50_2 + x_s80_2 + x_s100_2 + x_s150_2 + x_s200_2*/ + x_s700_2)/2;
     int cal_y_2 = (y_s_2 /*+ y_s30_2 + y_s50_2 + y_s80_2 + y_s100_2 + y_s150_2 + y_s200_2*/ + y_s700_2)/2;


     Point LINE2_P1(x_s500_2, y_s500_2);
     Point LINE2_P2(x_s_2,y_s_2);

     Mat mask = Mat::zeros(480, 640, CV_8UC1);



     //cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
     cv::line(mask, LINE1_P1, LINE1_P2, Scalar(255, 255, 255),1,LINE_AA,0);
     cv::line(mask, LINE2_P1, LINE2_P2, Scalar(255, 255, 255),1,LINE_AA,0);
     imshow("mask",mask);


     //HoughLineP 수행
     vector<Vec4i> lines;
     HoughLinesP(mask,lines,1,CV_PI/180,43,30,1);
     Mat dst;
     cvtColor(new_hull_img, dst, COLOR_GRAY2BGR);

     //cout << "line size: " << lines.size() << endl;

     /*
     for(Vec4i l : lines)
     {
         cv::line(dst, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,0,255),1,LINE_AA);
         float angle = atan2(l[1]-l[3],l[0]-l[2]);
         cout << "angle: " << angle << "P1_x: " <<l[0]<<",P1_y: "<<l[1]<<",  P2_x: "<<l[2]<<", P2_y: "<<l[3]<<endl;
     }
     */
        /*
         cv::line(dst, Point(lines[2][0],lines[2][1]), Point(lines[2][2],lines[2][3]), Scalar(0,0,255),1,LINE_AA);
         float angle = atan2(lines[2][3]-lines[2][1],lines[2][2]-lines[2][0]);
         cout << "angle: " << angle << "P1_x: " <<lines[0][0]<<",P1_y: "<<lines[0][1]<<",  P2_x: "<<lines[0][2]<<", P2_y: "<<lines[0][3]<<endl;

         cv::line(dst, Point(lines[1][0],lines[1][1]), Point(lines[1][2],lines[1][3]), Scalar(0,0,255),1,LINE_AA);
         float angle2 = atan2(lines[1][1]-lines[1][3],lines[1][0]-lines[1][2]);
         cout << "angle2: " << angle2 << "P1_2_x: " <<lines[1][0]<<",P1_2_y: "<<lines[1][1]<<",  P2_2_x: "<<lines[1][2]<<", P2_2_y: "<<lines[1][3]<<endl;


        //int(sin(double(L_ang * CV_PI/180.0))*10)
         int P1X = lines[2][0];
         int P1Y = lines[2][1];
         int P2X = P1X - 1000*cos(angle*(CV_PI/180));
         int P2Y = P1Y - 1000*sin(angle*(CV_PI/180));
         cv::line(dst, Point(P2X,P2Y), Point(P1X,P1Y), Scalar(0,255,0),1,LINE_AA);


         cv::imshow("dst",dst);
         */


     //Linefit Test (위에서 나온 Mask Mat에서 수행)
         cv::Vec4f line, line2;
         vector<vector<Point>> line_n;
         findContours( mask, line_n, hierarchy1, RETR_TREE, CHAIN_APPROX_NONE );
         //cout <<"fit line count"<<line_n.size()<<endl;


         cv::fitLine(line_n[0],line,CV_DIST_L2,0,0.01,0.01);
         int x0 = line[2];
         int y0 = line[3];
         int ly = int((-x0*(line[1]/line[0])+y0));
         int ry = int((img.cols-x0)*(line[1]/line[0])+y0);
         cv::line(img, Point(img.cols-1,ry), Point(0,ly), Scalar(255,0,0),2,LINE_AA);


         cv::fitLine(line_n[1],line2,CV_DIST_L2,0,0.01,0.01);
         int x1 = line2[2];
         int y1 = line2[3];
         int l2y = int((-x1*(line2[1]/line2[0])+y1));
         int r2y = int((img.cols-x1)*(line2[1]/line2[0])+y1);
         cv::line(img, Point(img.cols-1,r2y), Point(0,l2y), Scalar(255,0,0),2,LINE_AA);

         cv::imshow("dst",img);

         /*
         cv::fitLine(line_n[1],line2,CV_DIST_L2,0,0.01,0.01);
         int x0_2 = line2[2];
         int y0_2 = line2[3];
         int x1_2 = x0_2+line2[0]*1000;
         int y1_2 = y0_2+line2[1]*1000;
         cv::line(dst, Point(x0_2,y0_2), Point(x1_2,y1_2), Scalar(0,255,0),1,LINE_AA);
         cv::imshow("dst",dst);
         */

     /*
     int Next_Left_X = Start_X + int(cos(double(L_ang * CV_PI/180.0))*10);
     int Next_Left_Y = Start_Y + int(sin(double(L_ang * CV_PI/180.0))*10);
     Point P1_Left1(Start_X,Start_Y);
     Point P2_Left2(Next_Left_X,Next_Left_Y);
     cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
    */



     //cout << "x : " << x_e << endl;


    //테스트용

    /*Hough Line P 알고리즘으로 라인그리기.*/
    /*

    Mat InEdge;
    cv::Canny(new_hull_img,InEdge,220,255);
    cv::imshow("InEdge",InEdge);
    vector<Vec4i> lines;
    HoughLinesP(InEdge,lines,1,CV_PI/180,80,70,5);
    Mat dst;
    cvtColor(new_hull_img, dst, COLOR_GRAY2BGR);
    cout << "line size: " << lines.size() << endl;
    for(Vec4i l : lines)
    {
        cv::line(dst, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,0,255),2,LINE_AA);
    }
    cv::imshow("dst",dst);
    */





    /*Hough Line P + Linefit으로 검출된 Edge와 실제로 겹치는 부분만 그리기.*/
/*
    Mat InEdge;
    cv::Canny(new_hull_img,InEdge,220,255);
    cv::imshow("InEdge",InEdge);

    vector<Vec2f> lines;
    HoughLines(InEdge,lines,1,CV_PI/180,100);

    Mat dst;
    cvtColor(InEdge, dst, COLOR_GRAY2BGR);

    cout << "lines_size : " << lines.size() << endl;

    for(size_t i=0; i<lines.size(); i++)
    {
        float r = lines[i][0], t = lines[i][0];
        double cos_t = cos(t);
        double sin_t = sin(t);
        double x0 = r * cos_t;
        double y0 = r * sin_t;
        double alpha = 1000;

        Point pt1(cvRound(x0 + alpha*(-sin_t)), cvRound(y0 + alpha*cos_t));
        Point pt2(cvRound(x0 - alpha*(-sin_t)), cvRound(y0 - alpha*cos_t));
        line(dst, pt1, pt2, Scalar(0,0,255), 2, LINE_AA);
    }
    cv::imshow("dst",dst);
*/


    //Hough Line P
    /*
    Mat InEdge;
    cv::Canny(new_hull_img,InEdge,220,255);
    vector<Vec4i> lines;
    HoughLinesP(InEdge,lines,1,CV_PI/180,10,40,100);
    Mat HoughLinesP;
    HoughLinesP=new_hull_img.clone();
    //cout << "line size: " << lines.size() << endl;
    for(Vec4i l : lines)
    {

        cv::line(HoughLinesP, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(255,255,255),2,LINE_AA);
    }

    for(int i=0; i<lines.size(); i++)
    {
        //cout << i << "line, x0:"<<lines[i][0]<<", y0:"<<lines[i][1]<<", x1:"<<lines[i][2]<<", y1:"<<lines[i][3]<<endl;
    }
    cv::imshow("HoughLineP",HoughLinesP);
    cv::imwrite("HoughLineP.bmp",HoughLinesP);
    */






    // create hull array for convex hull points
    /*
    vector< vector<Point> > hull(contours_left.size());
    for(int i = 0; i < contours_left.size(); i++)
    {
        convexHull(Mat(contours_left[i]), hull[i], false, false);
    }
    // create a blank image (black image)
    Mat drawing = Mat::zeros(gray.size(), CV_8UC3);
    Scalar color_contours = Scalar(0, 0, 255); // color for contours
    Scalar color = Scalar(0, 255, 0); // color for convex hull
    drawContours(img, contours_left, 0, color_contours, 2, 8, vector<Vec4i>(), 0, Point());
    */
    //drawContours(img, hull, 0, color, 1, 8, vector<Vec4i>(), 0, Point());






    //approxPolyDP(Mat(contours_left), contours_left_dp, 3, true);
    //cv::drawContours(img,contours_left_dp,0,Scalar(255,255,0),2,LINE_8,hierarchy1);



    /*
    cout << "contour size: "<< contours_left.size() <<endl;
    vector<vector<Point>> hull(contours_left.size());
    convexHull(Mat(contours_left[0]),hull[0],true);
    cv::drawContours(img,hull,0,Scalar(0,0,255),1,LINE_8,hierarchy1);
    cv::imshow("contours_left",img);



    cout << "contour size: "<< contours_left[0].size() <<endl;
    cout << "hull size: "<< hull[0].size() <<endl;
    for(int i=0; i<hull[0].size(); i++)
    {
        cout << "hull_x: " << hull[0][i].x << endl;
        cout << "hull_y: " << hull[0][i].y << endl;
    }



    //contour => Mat convert
    Mat image_contours_grayscale = Mat::zeros(L_grad.size(),L_grad.type());
    Scalar color(255);
    cv::drawContours(image_contours_grayscale,hull,0,color,1,LINE_8,hierarchy1);
    cv::imshow("rebuilt",image_contours_grayscale);
    */

    vector<tuple<int, int, float>> data;
    vector<tuple<int, int, float>> data_mag;
    vector<pair<double,int>> com_ang, com_mag;
    vector<float> dev_data;

    vector<tuple<int, int, float>> data_dev, data_dev_cal; //각 Point에 대해서 좌우 미분차이값 저장 tuple.  data_dev : 데이터값저장,  data_dev_cal : 연산데이터(기준점 기준 좌우편차)

    int gx_h, gy_h, sum_h;

    int Pt_Size = contours_left[0].size();
    int cnt_pt=0;


    //원래는 test였는데, new_hull_img로 변경 (2021.08.30)
    for(int i=0; i<new_hull_img.rows; i++) //y
    {
        for(int j=0; j<new_hull_img.cols; j++) //x
        {

          float temp = new_hull_img.at<uchar>(i,j);
          if(temp > 120)
          {

              //if(i<=1) continue;
              //if(j>=639) continue;

              gx_h = xGradient(new_hull_img, j, i);
              gy_h = yGradient(new_hull_img, j, i);


              float l_mag = sqrt(pow(gx_h,2) + pow(gy_h,2));
              L_mag[i][j] = l_mag;
              data_mag.push_back(make_tuple(j,i,l_mag));

              float temp = atan2(gy_h,gx_h);
              temp = temp * (180.0/CV_PI);//Radian -> degree
              if (temp < 0.0) { //convert to -pi ~ +pi ---> 0~2pi
                  temp += 360.0;
              }
              dst_angle_left[i][j] = temp;
              data.push_back(make_tuple(j,i,temp));
              data_dev.push_back(make_tuple(j,i,0)); //x,y,data

            }
        }
    }











    for(int i=1; i<data.size()-1; i++)
    {

        float temp = DIFF_ABS(fabs(get<2>(data[i-1])),fabs(get<2>(data[i])));
        float temp2 = DIFF_ABS(fabs(get<2>(data[i])),fabs(get<2>(data[i+1])));
        float temp3 = DIFF_ABS(fabs(temp),fabs(temp2));
        //cout << "angle [" << i << "] dev: " << temp3 <<endl;

        com_ang.push_back(make_pair(temp3,i));
    }


    for(int i=1; i<data_mag.size()-1; i++)
    {

        float temp = DIFF_ABS(fabs(get<2>(data_mag[i-1])),fabs(get<2>(data_mag[i])));
        float temp2 = DIFF_ABS(fabs(get<2>(data_mag[i])),fabs(get<2>(data_mag[i+1])));
        float temp3 = DIFF_ABS(fabs(temp),fabs(temp2));
        //cout << "mag [" << i << "] dev: " << temp3 <<endl;

        com_mag.push_back(make_pair(temp3,i));

    }

    sort(com_ang.begin(), com_ang.end());
    for(int i=0; i<com_ang.size(); i++)
    {
        //cout << get<0>(com_ang[i]) << ":" <<  get<1>(com_ang[i]) <<"angle difference" << endl;
    }


    //cout << "angle max data, x :" << get<0>(data[com_ang.back().second]) << ", y :" << get<1>(data[com_ang.back().second]) << ", angle difference :" << get<0>(com_ang[com_ang.back().second]) << endl;
    //cout << "<--------------------------------------------------------------------->" << endl;
    sort(com_mag.begin(), com_mag.end());
    for(int i=0; i<com_mag.size(); i++)
    {
        //cout << get<0>(com_mag[i]) << ":" <<  get<1>(com_mag[i]) <<"magnitude difference"<< endl;
    }
    //cout << "angle max data, x :" << get<0>(data[com_ang.back().second]) << ", y :" << get<1>(data[com_ang.back().second]) << ", angle difference :" << get<0>(com_ang[com_ang.back().second]) << endl;
    //cout << "mag max data, x :" << get<0>(data[com_mag.back().second]) << ", y :" << get<1>(data[com_mag.back().second]) << ", mag difference :" << get<0>(com_ang[com_mag.back().second]) << endl;
    //cout << "contour 0 size" << contours_left[0].size() << endl;
    //cout << "contour [0][0].x" << contours_left[0][0].x << endl;



    /*
    cv::imshow("contours_left",img);
    Mat reshape_Left = Mat(L_grad.rows, L_grad.cols, CV_8UC1);
    cv::polylines(reshape_Left,hull,false,Scalar(255));
    cv::imshow("reshape_Left",reshape_Left);
    */




/*
    for(int i=0; i<reshape_Left.rows; i++)
    {
        for(int j=0; j<reshape_Left.cols; j++)
        {
            float temp = reshape_Left.at<uchar>(i,j);
            if((temp > 100) && (temp!=255))
            {
                reshape_Left.at<uchar>(i,j) = 255;
            }
        }
    }


    for(int i=0; i<R_grad.rows; i++)
    {
        for(int j=0; j<R_grad.cols; j++)
        {
            float temp = R_grad.at<uchar>(i,j);
            if((temp > 100) && (temp!=255))
            {
                R_grad.at<uchar>(i,j) = 255;
            }
        }
    }


    Mat L_SobelX_2, L_SobelY_2,ABS_L_SobelX_2,ABS_L_SobelY_2;
    cv::Sobel(reshape_Left, L_SobelX_2, CV_16S, 1,0,0); //output depth : 16bit signed integer
    cv::Sobel(reshape_Left, L_SobelY_2, CV_16S, 0,1,0);
    //CV_16S -> CV_8U (8bit unsigned integer)
    cv::convertScaleAbs(L_SobelX_2, ABS_L_SobelX_2);
    cv::convertScaleAbs(L_SobelY_2, ABS_L_SobelY_2);


    Mat L_grad_2,R_grad_2;
    cv::addWeighted(ABS_L_SobelX_2,0.5,ABS_L_SobelY_2,0.5,0,L_grad_2);
*/





/*

    for(int i=0; i<L_grad_2.rows; i++)
    {
        for(int j=0; j<L_grad_2.cols; j++)
        {

            float temp = L_grad_2.at<uchar>(i,j);
            if(temp>100)
            {
                //Magnitude
                float l_mag_x = ABS_L_SobelX_2.at<uchar>(i,j);
                float l_mag_y = ABS_L_SobelY_2.at<uchar>(i,j);
                float l_mag = sqrt(pow(l_mag_x,2) + pow(l_mag_y,2));
                L_mag[i][j] = l_mag;

                //Angle
                float temp = atan2(l_mag_y,l_mag_x);
                temp = temp * (180.0/CV_PI);//Radian -> degree
                if (temp < 0.0) { //convert to -pi ~ +pi ---> 0~2pi
                    temp += 360.0;
                }
                dst_angle_left[i][j] = temp;
            }

        }
    }





    for(int i=0; i<R_grad.rows; i++)
    {
        for(int j=0; j<R_grad.cols; j++)
        {
            float temp = R_grad.at<uchar>(i,j);
            if(temp>100)
            {
                //Magnitude
                float r_mag_x = ABS_R_SobleX.at<uchar>(i,j);
                float r_mag_y = ABS_R_SobleY.at<uchar>(i,j);
                float r_mag = sqrt(pow(r_mag_x,2) + pow(r_mag_y,2));
                R_mag[i][j] = r_mag;


                //Angle
                float temp2 = atan2(r_mag_y,r_mag_x);
                temp2 = temp2 * (180.0/CV_PI);//Radian -> degree
                if (temp2 < 0.0) { //convert to -pi ~ +pi ---> 0~2pi
                    temp2 += 360.0;
                }
                dst_angle_right[i][j] = temp2;
            }
        }
    }
    */



    int lineType = 8;
    int thickness = 1;
    double tipLength = 0.1;
    int cnt,cnt2=0;

    /*******************************************************************************************************************/
    //Left Cam1

    for(int i=0; i<new_hull_img.rows; i++)
    {
        for(int j=0; j<new_hull_img.cols; j++)
        {


            float temp = new_hull_img.at<uchar>(i,j);
            if(temp>=170 && temp!=0)
            {
                if(cnt%10==0)
                {

                    float L_ang = dst_angle_left[i][j];


                    //ang == 0
                    if(L_ang==0)
                    {
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X + int(cos(double(L_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y;
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang > 0 && ang < 90
                    else if(L_ang > 0 && L_ang < 90)
                    {
                        L_ang = L_ang+90;
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X + int(cos(double(L_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y + int(sin(double(L_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang == 90
                    else if(L_ang == 90)
                    {
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X;
                        int Next_Left_Y = Start_Y + int(sin(double(L_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang > 90 && ang < 180
                    else if(L_ang > 90 && L_ang < 180)
                    {
                        L_ang = L_ang+90;
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X - int(cos(double(L_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y + int(sin(double(L_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang == 180
                    else if(L_ang == 180)
                    {
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X - int(cos(double(L_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y;
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang > 180 && ang < 270
                    else if(L_ang > 180 && L_ang < 270)
                    {
                        L_ang = L_ang+90;
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X - int(cos(double(L_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y - int(sin(double(L_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang == 270
                    else if(L_ang == 270)
                    {

                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X;
                        int Next_Left_Y = Start_Y - int(sin(double(L_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang > 270 && ang < 360
                    else if(L_ang > 270 && L_ang < 360)
                    {
                        L_ang = L_ang+90;
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X + int(cos(double(L_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y - int(sin(double(L_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }



                    //최종 Point 표시
                    Point P1_Ex1(get<0>(data[com_ang.back().second]),get<1>(data[com_ang.back().second]));
                    ExtremePoint = P1_Ex1;

                    //cv::arrowedLine(img, P1_Ex1, P1_Ex1, Scalar(255, 0, 0), 10, lineType, 0, 0);
                    cv::drawMarker(img, ExtremePoint, Scalar(0,0,255),MARKER_CROSS,10,2);

                    //talewidget data write
                    //ui->tableWidget->insertRow(ui->tableWidget->rowCount());
                    /*
                    QString s;
                    s = "(";
                    s += QString::number(j);
                    s += ",";
                    s += QString::number(i);
                    s += ")";
                    ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,0,new QTableWidgetItem(s));
                    ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,1,new QTableWidgetItem(QString::number(L_mag[i][j])));
                    ui->tableWidget->setItem(ui->tableWidget->rowCount()-1,2,new QTableWidgetItem(QString::number(dst_angle_left[i][j])));
                    */

                }
                cnt++;
            }


        }
    }

    /*******************************************************************************************************************/

    /*******************************************************************************************************************/
    //Left Cam1. 추후 아래 Left -> Right 변수명 수정해야함.
    /*
    for(int i=0; i<R_grad.rows; i++)
    {
        for(int j=0; j<R_grad.cols; j++)
        {


            float temp = R_grad.at<uchar>(i,j);
            if(temp > 100)
            {
                if(cnt2%10==0)
                {

                    float R_ang = dst_angle_right[i][j];


                    //ang == 0
                    if(R_ang==0)
                    {
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X + int(cos(double(R_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y;
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img2, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang > 0 && ang < 90
                    else if(R_ang > 0 && R_ang < 90)
                    {
                        //R_ang = R_ang;
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X + int(cos(double(R_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y + int(sin(double(R_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img2, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang == 90
                    else if(R_ang == 90)
                    {
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X;
                        int Next_Left_Y = Start_Y + int(sin(double(R_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img2, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang > 90 && ang < 180
                    else if(R_ang > 90 && R_ang < 180)
                    {
                        //R_ang = 360-R_ang;
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X - int(cos(double(R_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y + int(sin(double(R_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img2, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang == 180
                    else if(R_ang == 180)
                    {
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X - int(cos(double(R_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y;
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img2, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang > 180 && ang < 270
                    else if(R_ang > 180 && R_ang < 270)
                    {
                        //R_ang = 360-R_ang;
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X - int(cos(double(R_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y - int(sin(double(R_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img2, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang == 270
                    else if(R_ang == 270)
                    {

                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X;
                        int Next_Left_Y = Start_Y - int(sin(double(R_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img2, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }
                    //ang > 270 && ang < 360
                    else if(R_ang > 270 && R_ang < 360)
                    {
                        //R_ang = 360-R_ang;
                        int Start_X = j;
                        int Start_Y = i;
                        int Next_Left_X = Start_X + int(cos(double(R_ang * CV_PI/180.0))*10);
                        int Next_Left_Y = Start_Y - int(sin(double(R_ang * CV_PI/180.0))*10);
                        Point P1_Left1(Start_X,Start_Y);
                        Point P2_Left2(Next_Left_X,Next_Left_Y);
                        cv::arrowedLine(img2, P1_Left1, P2_Left2, Scalar(255, 0, 0), thickness, lineType, 0, 0);
                    }

                    //talewidget data write
                    ui->tableWidget_2->insertRow(ui->tableWidget_2->rowCount());
                    QString s;
                    s = "(";
                    s += QString::number(j);
                    s += ",";
                    s += QString::number(i);
                    s += ")";
                    ui->tableWidget_2->setItem(ui->tableWidget_2->rowCount()-1,0,new QTableWidgetItem(s));
                    ui->tableWidget_2->setItem(ui->tableWidget_2->rowCount()-1,1,new QTableWidgetItem(QString::number(R_mag[i][j])));
                    ui->tableWidget_2->setItem(ui->tableWidget_2->rowCount()-1,2,new QTableWidgetItem(QString::number(dst_angle_right[i][j])));


                }
                cnt2++;
            }


        }
    }
    */
    /*******************************************************************************************************************/






    /*
    Mat drawing = Mat::zeros( L_grad.size(), CV_8UC3 );
    Mat drawing2 = Mat::zeros( R_grad.size(), CV_8UC3 );

    Scalar color = Scalar(0, 255, 0);
    */

    ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(img.data,img.cols,img.rows,img.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
    //ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(img2.data,img2.cols,img2.rows,img2.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));




}





void MainWindow::on_btnCalibrate_clicked()
{
    //Calibration: Timer에서 처리

    //1. Align, PLC Thread 구동 체크. Thread 구동 시 Calibration 방지
    if(!worker_Align->bStatusAlignPro || !worker_PLC->bStatusPLCPro || m_CaliTimer->isActive()){
        return;
    }

    //2. Timer 생성
    //Calibration Timer
    m_CaliTimer  = make_shared<QTimer>();
    connect(m_CaliTimer.get(), SIGNAL(timeout()), this, SLOT(OnTimerCallbackFunc_Calibration()));
    m_CaliTimer->start();

    //3. STEP Initialize
    SetCalStep(CALI_STEP1);
    bcal_flag=true;

}


void MainWindow::on_pushButton_2_clicked()
{

    QString a = "Test";
    QString sLogMsg = SetLogSave(a);
    this->display_log(sLogMsg);




}
void MainWindow::readACK(QString str)
{
    return_msg = str;
}

void MainWindow::set_calculatedValues()
{
    //cout << "Test" << endl;
}

void MainWindow::display_log(QString sLogMsg)
{
    ui->edtLog->appendPlainText(sLogMsg);
    QWidget::update();
}


void MainWindow::on_btnStop_clicked()
{
    //if(bThreadStatus){return;}
    //bThreadStatus = false;
    worker_Align->bStatusAlignPro = true;
    worker_PLC->bStatusPLCPro = true;

    //cout << "StopButtonClick" << endl;

}


void MainWindow::on_btnStart_clicked()
{
    //cout << "StartButtonClick" << endl;

    if(!bAlignStartReq && bAlignComplete){
        bAlignStartReq=true;
        bAlignComplete=false;
    }else{
        return;
    }

    //    //Work방식 (Test result : ok)
    //    //Refer Link
    //    //https://doc.qt.io/qt-5/qthread.html#details
    //    //https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/
    worker_Align->bStatusAlignPro = false;
    worker_PLC->bStatusPLCPro = false;


    /**********************************************************************************************/
    worker_Align->moveToThread(thread_Align);

    //Worker의 Error Message를 Main Thread의 Error처리기능에 연결.
    //connect(thread, SIGNAL(error(QString)), this, SLOT(errorString(QSting)));
    //Thread의 시작신호를 Worker의 Process SLOT에 연결
    connect(thread_Align, SIGNAL(started()), worker_Align, SLOT(process()));
    //worker인스턴스가 finish를 방출(emit)하면, Thread 종료하도록 신호보냄.(shut down)
    connect(worker_Align, SIGNAL(finished()), thread_Align, SLOT(quit()));
    //worker instance에도 똑같이 finish 시 삭제하게끔 한다.
    connect(worker_Align, SIGNAL(finished()), worker_Align, SLOT(deleteLater()));
    //삭제 시 스레드가 완전히 종료되지 않아 심각한 충돌이 발생하지 않도록 하기위해, Thread의 finished를 deleteLater()에 연결
    connect(thread_Align, SIGNAL(finished()), worker_Align, SLOT(deleteLater()));

    //Run Thread
    thread_Align->start();

    /**********************************************************************************************/

    /**********************************************************************************************/
    worker_PLC->moveToThread(thread_PLC);

    //Worker의 Error Message를 Main Thread의 Error처리기능에 연결.
    //connect(thread, SIGNAL(error(QString)), this, SLOT(errorString(QSting)));
    //Thread의 시작신호를 Worker의 Process SLOT에 연결
    connect(thread_PLC, SIGNAL(started()), worker_PLC, SLOT(process()));
    //worker인스턴스가 finish를 방출(emit)하면, Thread 종료하도록 신호보냄.(shut down)
    connect(worker_PLC, SIGNAL(finished()), thread_PLC, SLOT(quit()));
    //worker instance에도 똑같이 finish 시 삭제하게끔 한다.
    connect(worker_PLC, SIGNAL(finished()), worker_PLC, SLOT(deleteLater()));
    //삭제 시 스레드가 완전히 종료되지 않아 심각한 충돌이 발생하지 않도록 하기위해, Thread의 finished를 deleteLater()에 연결
    connect(thread_PLC, SIGNAL(finished()), worker_PLC, SLOT(deleteLater()));

    //Run Thread
    thread_PLC->start();
    /**********************************************************************************************/

}


// Drawing
//여기서 Drawing, update는 외부의 함수에서  QWidget::update(); 사용.
void MainWindow::paintEvent(QPaintEvent *event)
{

    /***************************************************************/
//    QString filename = "C:/contour_L.jpg";
//    Mat img = cv::imread(filename.toStdString());

//    char repaint_test_var_char[10];
//    sprintf_s(repaint_test_var_char, "X: %d",repaint_test_var);
//    putText(img, repaint_test_var_char, Point(20,20),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);
//    QPainter painter(this);
//    ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(img.data,img.cols,img.rows,img.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height())));
//    QWidget::paintEvent(event);
    /***************************************************************/


    /*
    QString filename = "C:/contour_L.bmp";
    QString filename2 = "C:/contour_R.bmp";
    Mat input_1 = cv::imread(filename.toStdString());
    Mat input_2 = cv::imread(filename2.toStdString());

    Mat out1,out2;
    bool result;
    CoorData cam1_coor, cam2_coor;


    result = test->FindVirtualPoint(input_1,input_2,&out1,&out2, &cam1_coor, &cam2_coor);

    char repaint_test_var_char[10];
    sprintf_s(repaint_test_var_char, "X: %d",repaint_test_var);
    putText(out1, repaint_test_var_char, Point(20,20),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);
    putText(out2, repaint_test_var_char, Point(20,20),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);

    QPainter painter(this);

    if(result){
        ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(out1.data,out1.cols,out1.rows,out1.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height())));
        ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(out2.data,out2.cols,out2.rows,out2.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height())));
    }
    */

    QWidget::paintEvent(event);


}

void MainWindow::on_pushButton_3_clicked()
{
    repaint_test_var++;

    QWidget::update(); //Main 화면 UI Widget update command

}

void MainWindow::OnTimerCallbackFunc()
{
    repaint_test_var++;

    QWidget::update(); //Main 화면 UI Widget update command
}

QString MainWindow::_Pulse2MM(double pul)
{
    QString str;
    pul /= PPR;
    str = QString::number(pul, 'd', 4);
    return str;
}

double MainWindow::_Pix2MM(double pix)
{
    double mm;
    //mm = pix * align.GetPixResolution();
    return mm;
}



void MainWindow::SetPulse(double *p, int x1, int x2, int y)
{
    /*
     * Goal:    Set motor pusle values. Show on UI. And let UVW move.
     * Input:   Pulse array; X1 pulse; X2 pulse; Y pulse
     */


    ui->edt_motor_x1->setText(QString::number(_Pulse2MM(x1).toDouble(),'d',3));
    ui->edt_motor_x2->setText(QString::number(_Pulse2MM(x2).toDouble(),'d',3));
    ui->edt_motor_Y->setText(QString::number(_Pulse2MM(y).toDouble(),'d',3));

    if (p){
        p[0] = (double)x1;
        p[1] = (double)x2;
        p[2] = (double)y;
    }
}

QString MainWindow::ControlPLC(Communication *com, QString mode, double *pul)
{
    /*
     * Goal:    to control PLC by pulse.
     * Input:   PLC socket[Communication]; mode: 'Abs', 'Rel', 'Deg'
     *          'Home', 'Zero'; pulse values [double[]]
     * Output:  The message which PLC send back.
     */
    QString command = "";
    QString return_str = "Null";
    if (mode == "Abs" || mode == "Rel"){
        QString p1 = _Pulse2MM(pul[0]);
        QString p2 = _Pulse2MM(pul[1]);
        QString p3 = _Pulse2MM(pul[2]);
        command = QString("REQ,%1,%2,%3,%4").arg(mode).arg(p1).arg(p2).arg(p3);
    }
    else if (mode == "Deg"){
        QString deg = QString::number(pul[0], 'd', 3);
        command = QString("REQ,%1,%2").arg(mode).arg(deg);
    }
    else if (mode == "Zero"){
        command = QString("REQ,%1,%2,%3,%4").arg("Abs").arg("0").arg("0").arg("0");
    }
    else{
        command = QString("REQ,%1").arg(mode);
    }
    return_str = com->Send(command);

    if (bcal_flag)
        QThread::usleep(350000);
    else
        QThread::usleep(100000);

    return com->Read();
}



void MainWindow::OnTimerCallbackFunc_Calibration()
{

    while(bcal_flag)
    {

        //STEP1: Parameter Read and Measure current position
        if(GetCalStep() == CALI_STEP1){
            QString sLogMsg = SetLogSave("Calibration Process: CALI_STEP1");
            this->display_log(sLogMsg);

            Mat in_frame_cam1, in_frame_cam2, out_frame_cam1, out_frame_cam2;
            bool result;
            CoorData cam1_coor, cam2_coor;

            //측정
            result = test->FindVirtualPoint(in_frame_cam1,in_frame_cam2,&out_frame_cam1,&out_frame_cam1, &cam1_coor, &cam2_coor);

            //1번 cam detec pos data insert to vector
            CoorData detect_pos;
            detect_pos.x = (double)cam1_coor.x;
            //detect_pos.y = (double)(row value of camera resoultion - cam1_coor.y); //왜냐하면 좌표계(0,0)이 Bottom-Left
            detect_pos.y = (double)500; //Test Value. 왜냐하면 Camera, Lens가 정해지지 않음.

            if(detect_pos.x && detect_pos.x)
            {
                cal_pos.push_back(detect_pos);
            }
            else
            {
                //Treat Exception.
                m_CaliTimer->stop();
                break;

            }

            //2번 cam detec pos data insert to vector
            detect_pos.x = (double)cam2_coor.x;
            detect_pos.y = (double)500;
            if(detect_pos.x && detect_pos.x)
            {
                cal_pos.push_back(detect_pos);
            }
            else
            {
                //Treat Exception.
                m_CaliTimer->stop();
                break;
            }

            SetCalStep(CALI_STEP2);

        }

        //STEP2: Motor Moving
        if(GetCalStep() == CALI_STEP2){
            QString sLogMsg = SetLogSave("Calibration Process: CALI_STEP2");
            this->display_log(sLogMsg);

            int dis = (int) (PPR * worker_Align->GetDistanceCal());
            double pulse[3] = {0.0, 0.0, 0.0};



            if(count_calpos == 0)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                SetPulse(pulse, 0.0, 0.0, -dis);
                ControlPLC(com, "Abs", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 1)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                SetPulse(pulse, -dis, dis, -dis);
                ControlPLC(com, "Abs", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 2)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                SetPulse(pulse, -dis, dis, 0.0);
                ControlPLC(com, "Abs", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 3)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                SetPulse(pulse, -dis, dis, dis);
                ControlPLC(com, "Abs", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 4)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                SetPulse(pulse, 0.0, 0.0, dis);
                ControlPLC(com, "Abs", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 5)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                SetPulse(pulse, dis, -dis, dis);
                ControlPLC(com, "Abs", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 6)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                SetPulse(pulse, dis, -dis, 0.0);
                ControlPLC(com, "Abs", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 7)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                SetPulse(pulse, dis, -dis, -dis);
                ControlPLC(com, "Abs", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 8)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                ControlPLC(com, "Zero", nullptr);
                ui->edt_motor_degree->setText("1");

                pulse[0] = worker_Align->GetAngCal();
                ControlPLC(com, "Deg", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 9)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                ui->edt_motor_degree->setText("-2");

                pulse[1] = worker_Align->GetAngCal();
                ControlPLC(com, "Deg", pulse);

                SetCalStep(CALI_STEP1);
                count_calpos++;
                continue;
            }
            else if(count_calpos == 10)
            {
                QString s_count_calpos = QString::number(count_calpos+1);
                QString sLogMsg = SetLogSave("Calibration:\n"+s_count_calpos);
                this->display_log(sLogMsg);

                ControlPLC(com, "Zero", nullptr);

                SetCalStep(CALI_STEP3);
                count_calpos++;
                continue;
            }
        }


        //STEP3: Calibration Parameter calculation
        if(GetCalStep() == CALI_STEP3){
            //Calcaulation Calibtraton parameter
            worker_Align->SetPosCal(cal_pos); //위에서 측정한 Cal Position -> AlignPrcoess Cal Position
            worker_Align->SolvePul2Pix(); //get the "l"
            worker_Align->RunCalibration(); //get the "c1", "c2" and adjust origin position of l2 to l1

            //Get the pc1, pc2
            pc = worker_Align->GetPlatCenter();
            pc2 = worker_Align->GetPlatCenter2();

            //Save Calibration Parameter to INI File???


            count_calpos = 0;
            bcal_flag = false;

            //UI Display, Log Save


            m_CaliTimer->stop();
            break;
        }
    }
}




void MainWindow::on_pushButton_4_clicked()
{
    QString filename = "D:/contour_L.bmp";
    Mat input = cv::imread(filename.toStdString(), IMREAD_GRAYSCALE);
    Mat dst, cdst, cdstP;

    Mat img, img2, gray, result_el;

    //Result Coordinates
    CoorData coor_result_1, coor_result_2;
    unsigned int x_c1, y_c1, x_c2, y_c2;

    //Image Load and noise remove
    /*****************************************************/
    img = cv::imread(filename.toStdString());
    cv::cvtColor(img,gray,CV_BGR2GRAY);
    cv::GaussianBlur(gray,gray,Size(5,5),0,0);
    cv::threshold(gray,gray,45,255,THRESH_BINARY);
    /*****************************************************/
    //Erode and dilate
    /*****************************************************/
    //Closing Process(dilate -> erode)
    cv::dilate(gray,result_el,Mat::ones(Size(5,5),CV_8UC1),Point(-1,-1),5); //modify iteration 2->5 2021.06.22
    cv::erode(result_el,result_el,Mat::ones(Size(5,5),CV_8UC1),Point(-1,-1),5);
    /*****************************************************/


    //Find Contour
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    vector<Point> final_con_pt_x;//Point vector for one contour obtained after find contour(x cordinate)
    vector<Point> final_con_pt_y;//Point vector for one contour obtained after find contour(y cordinate)

    /********************************************************************************/
    findContours(result_el,contours,hierarchy,RETR_EXTERNAL,CHAIN_APPROX_SIMPLE);
    final_con_pt_x.clear();
    final_con_pt_x.assign(contours[0].begin(), contours[0].end());
    final_con_pt_y.clear();
    final_con_pt_y.assign(contours[0].begin(), contours[0].end());
    /********************************************************************************/


    //4. Sorting Contour Points
//    std::sort(final_con_pt_x.begin(), final_con_pt_x.end(), myobject_x);
//    std::sort(final_con_pt_y.begin(), final_con_pt_y.end(), myobject_y);


    int idx=0, largestComp=0;
    double maxArea=0;
    char Val_detect_x[10];
    char Val_detect_y[10];

    for( ; idx>=0; idx=hierarchy[idx][0]){
        const vector<Point>& c = contours[idx];
        double area = fabs(contourArea(Mat(c)));
        if(area > maxArea)
        {
            maxArea = area;
            largestComp = idx;
        }
    }

    cv::Point2d pt_left, pt_right;

    pt_left.x = final_con_pt_x.front().x;
    pt_left.y = final_con_pt_x.front().y;

    pt_right.x = final_con_pt_x.back().x;
    pt_right.y = final_con_pt_x.back().y;


    //cout << "final_con_pt_x.back " << final_con_pt_x.back() << endl;



    cv::drawContours(img, contours, largestComp, Scalar(255,0,255), 1);
    cv::drawMarker(img, pt_left, Scalar(0,0,255),MARKER_TILTED_CROSS,10,2);
    cv::drawMarker(img, pt_right, Scalar(0,255,0),MARKER_TILTED_CROSS,10,2);

    //cv::drawMarker(img, final_con_pt_x.back(), Scalar(0,0,255),MARKER_TILTED_CROSS,10,2);


    //5. draw the contour and virtual point at Mat
    /***********************************************************************************************/
//    cv::drawContours(img, contours, largestComp, Scalar(255,0,255), 1);
//    cv::drawMarker(img, final_con_pt_x.front(), Scalar(0,0,255),MARKER_TILTED_CROSS,10,2);
//    cv::drawMarker(img, final_con_pt_y.back(), Scalar(0,0,255),MARKER_TILTED_CROSS,10,2);

//    cv::line(img, Point(final_con_pt_x.front().x, 0), Point(final_con_pt_x.front().x, 480),Scalar(0,0,255),3);
//    cv::line(img, Point(0, final_con_pt_y.back().y), Point(640, final_con_pt_y.back().y),Scalar(0,0,255),3);

//    cv::drawMarker(img, Point(final_con_pt_x.front().x, final_con_pt_y.back().y), Scalar(0,255,0),MARKER_CROSS,10,2);


//    sprintf_s(Val_detect_x, "X: %d",final_con_pt_x.front().x);
//    sprintf_s(Val_detect_y, "Y: %d",final_con_pt_y.back().y);


//    x_c1 = final_con_pt_x.front().x;
//    y_c1 = final_con_pt_y.back().y;

//    coor_result_1.x = x_c1;
//    coor_result_1.y = y_c1;

//    cv::putText(img, Val_detect_x, Point(50,410),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);
//    cv::putText(img, Val_detect_y, Point(50,430),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);




    cv::cvtColor(img,img,CV_BGR2RGB); //Opencv Mat -> Qt QImage Data Transform
    /***********************************************************************************************/

    imshow("Result",img);
    cv::waitKey(0);



}


void MainWindow::on_btn_median_clicked()
{
    Mat src, dst;

    // Load an image
    src = imread("D:/Median_Test.jpg", CV_LOAD_IMAGE_GRAYSCALE);

      if( !src.data )
      {
          //cout << "can not load image!" << endl;
      }


      //create a sliding window of size 9
      int window[9];

        dst = src.clone();
        for(int y = 0; y < src.rows; y++)
            for(int x = 0; x < src.cols; x++)
                dst.at<uchar>(y,x) = 0.0;

        for(int y = 1; y < src.rows - 1; y++){
            for(int x = 1; x < src.cols - 1; x++){

                // Pick up window element

                window[0] = src.at<uchar>(y - 1 ,x - 1);
                window[1] = src.at<uchar>(y, x - 1);
                window[2] = src.at<uchar>(y + 1, x - 1);
                window[3] = src.at<uchar>(y - 1, x);
                window[4] = src.at<uchar>(y, x);
                window[5] = src.at<uchar>(y + 1, x);
                window[6] = src.at<uchar>(y - 1, x + 1);
                window[7] = src.at<uchar>(y, x + 1);
                window[8] = src.at<uchar>(y + 1, x + 1);

                // sort the window to find median
                insertionSort(window);

                // assign the median to centered element of the matrix
                dst.at<uchar>(y,x) = window[4];
            }
        }

        namedWindow("final");
        imshow("final", dst);

        namedWindow("initial");
        imshow("initial", src);
}

//sort the window using insertion sort
//insertion sort is best for this sorting
void MainWindow::insertionSort(int window[])
{
    int temp, i , j;
    for(i = 0; i < 21; i++){
        temp = window[i];
        for(j = i-1; j >= 0 && temp < window[j]; j--){
            window[j+1] = window[j];
        }
        window[j+1] = temp;
    }
}


void MainWindow::on_table_Left_cellChanged(int row, int column)
{

}


void MainWindow::on_table_right_cellChanged(int row, int column)
{

}


void MainWindow::on_btnRotation_clicked()
{

    if(!bTestRot) return;

    QString filename = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
    QString filename2 = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));

    img = cv::imread(filename.toStdString());
    img2 = cv::imread(filename2.toStdString());

    //double angle = 1;
    //edttestangle.text()
    QString text = ui->edttestangle->text();
    double angle = text.toFloat();

    //get the rotation matrix for rotation the image around it's center in pixel coordinate
    cv::Point2f center((img.cols - 1) / 2.0, (img.rows - 1) / 2.0);
    cv::Point2f center2((img2.cols - 1) / 2.0, (img2.rows - 1) / 2.0);


    cv::Mat rot = cv::getRotationMatrix2D(center, angle, 1.0);
    cv::Mat rot2 = cv::getRotationMatrix2D(center2, angle, 1.0);



    //cout << "image size: " << img.size() <<endl;

    //originial image size 640 x 480 -> 670 x 510 (Roatation 시 corner 부분 cut 방지)

    int upper_size_width = 670;
    int upper_size_height = 510;

    //cv::Rect2f bbox = cv::RotatedRect(cv::Point2f(), img.size(), angle).boundingRect2f();
    cv::Rect2f bbox = cv::RotatedRect(cv::Point2f(), Size(upper_size_width, upper_size_height), angle).boundingRect2f();
    cv::Rect2f bbox2 = cv::RotatedRect(cv::Point2f(), img2.size(), angle).boundingRect2f();


    rot.at<double>(0, 2) += bbox.width / 2.0 - img.cols / 2.0;
    rot.at<double>(1, 2) += bbox.height / 2.0 - img.rows / 2.0;

    rot2.at<double>(0, 2) += bbox2.width / 2.0 - img2.cols / 2.0;
    rot2.at<double>(1, 2) += bbox2.height / 2.0 - img2.rows / 2.0;


    cv::warpAffine(img, img, rot, bbox.size());
    cv::warpAffine(img2, img2, rot, img2.size());




}


void MainWindow::on_bRotationUse_stateChanged(int arg1)
{
    //Check the function of Roation
    if(arg1==2) //checked
    {
        bTestRot = true;
    }
    else if(arg1==0) //unchecked
    {
        bTestRot = false;

    }
}


void MainWindow::on_pushButton_5_clicked()
{

}

// Computes the x component of the gradient vector
// at a given point in a image.
// returns gradient in the x direction
int MainWindow::xGradient(Mat image, int x, int y)
{
    return image.at<uchar>(y-1, x-1) +
           2*image.at<uchar>(y, x-1) +
           image.at<uchar>(y+1, x-1) -
           image.at<uchar>(y-1, x+1) -
           2*image.at<uchar>(y, x+1) -
           image.at<uchar>(y+1, x+1);
}

// Computes the y component of the gradient vector
// at a given point in a image
// returns gradient in the y direction

int MainWindow::yGradient(Mat image, int x, int y)
{
    return image.at<uchar>(y-1, x-1) +
           2*image.at<uchar>(y-1, x) +
           image.at<uchar>(y-1, x+1) -
           image.at<uchar>(y+1, x-1) -
           2*image.at<uchar>(y+1, x) -
            image.at<uchar>(y+1, x+1);
}

void MainWindow::on_pushButton_6_clicked()
{
    if(!img.empty())
    {
        cv::drawMarker(img_clone, ExtremePoint, Scalar(0,0,255),MARKER_CROSS,10,3);
        cv::imwrite("C:/Users/tommy/Documents/build-ShapeAlignmentSystem-Desktop_Qt_5_12_11_MinGW_32_bit-Debug/Test Image/PanelEdge/PanelEdge/SaveOrgPos.bmp",img_clone);
        //C:/Users/tommy/Documents/build-ShapeAlignmentSystem-Desktop_Qt_5_12_11_MinGW_32_bit-Debug/Test Image/PanelEdge/PanelEdge/SaveOrgPos.bmp

    }



}


//Hough line method
void MainWindow::on_pushButton_7_clicked()
{

    QString filename = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
    QString filename2 = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
    img = cv::imread(filename.toStdString());
    img2 = cv::imread(filename2.toStdString());

    Mat gray, result_el;
    Mat gray2, result_el2;
    Mat img_blur1, img_blur2;


    cv::cvtColor(img,gray,CV_BGR2GRAY);
    cv::GaussianBlur(img,img,Size(7,7),2,2);
    cv::threshold(gray,gray,47,255,THRESH_BINARY);
    cv::dilate(gray,gray,Mat::ones(Size(9,9),CV_8UC1),Point(-1,-1),3);

    cv::imshow("gray",gray);




    cv::GaussianBlur(img,img,Size(7,7),2,2);

    cv::cvtColor(img,gray,CV_BGR2GRAY);
    //cv::GaussianBlur(img,img,Size(3,3),2,1);
    cv::threshold(gray,gray,45,255,THRESH_BINARY);
    gray = ~gray;

    cv::erode(gray,gray,Mat::ones(Size(7,7),CV_8UC1),Point(-1,-1),2);
    Mat fgray = gray.clone();
    //gray = ~gray;
    cv::imshow("fgray",fgray);
    Mat transM;
    Mat k = cv::getStructuringElement(cv::MORPH_RECT, Size(7,7));
    cv::morphologyEx( fgray, transM, MORPH_OPEN, k );
    cv::imshow("transM",transM);
    cv::dilate(transM,transM,Mat::ones(Size(7,7),CV_8UC1),Point(-1,-1),2);



    /*
    cv::GaussianBlur(img,img,Size(7,7),2,2);
    cv::threshold(gray,gray,50,255,THRESH_BINARY);
    gray = ~gray;

    cv::erode(gray,gray,Mat::ones(Size(5,5),CV_8UC1),Point(-1,-1),1);
    Mat fgray = gray.clone();
    gray = ~gray;

    Mat transM;
    Mat k = cv::getStructuringElement(cv::MORPH_RECT, Size(15,15));
    cv::morphologyEx( fgray, transM, MORPH_OPEN, k );

    cv::dilate(transM,transM,Mat::ones(Size(5,5),CV_8UC1),Point(-1,-1),2);
    cv::imshow("transM_A",transM);
    */
    // Edge detection





    Mat dst,cdst,cdstP;
    Canny(TestHough, dst, 45, 255);



    // Standard Hough Line Transform
    vector<Vec2f> lines; // will hold the results of the detection
    HoughLines(dst, lines, 1, 3*CV_PI/180, 100, 0, 0 ); // runs the actual detection
    // Draw the lines

    for( size_t i = 0; i < lines.size(); i++ )
    {
       float rho = lines[i][0], theta = lines[i][1];
       Point pt1, pt2;
       double a = cos(theta), b = sin(theta);
       double x0 = a*rho, y0 = b*rho;
       pt1.x = cvRound(x0 + 1000*(-b));
       pt1.y = cvRound(y0 + 1000*(a));
       pt2.x = cvRound(x0 - 1000*(-b));
       pt2.y = cvRound(y0 - 1000*(a));
       line( img, pt1, pt2, Scalar(0,0,255), 3, LINE_AA);
    }


    //확률적기반 Hough line
    vector<Vec4i> linesP;
    HoughLinesP(dst, linesP, 1, CV_PI/180, 100, 100,20); // runs the actual detection
    Mat out_m;
    cvtColor(dst,out_m,COLOR_GRAY2BGR);





    for(Vec4i l : linesP)
    {
        cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);
       // cout << "l[0]: " << l[0] << ", l[1]: " << l[1] <<", l[2]: "<< l[2] << ", l[3]: " << l[3] << endl;

        double radian = atan2(l[1]-l[3], l[0]-l[2]);
        double degree = radian * 180 / CV_PI; // 라디안 -> 디그리 변환

        //수평선
        /*
        if((degree>=0)&&(degree<45)){cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);}
        if((degree>=135)&&(degree<180)){cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);}
        if((degree<0)&&(degree>=-45)){cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);}
        if((degree<-135)&&(degree>=-180)){cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);}
        */
        //수직선
        /*
        if((degree>=45)&&(degree<90)){cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);}
        if((degree>=90)&&(degree<135)){cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);}
        if((degree<-45)&&(degree>=-90)){cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);}
        if((degree<-90)&&(degree>=-135)){cv::line(out_m, Point(l[0],l[1]), Point(l[2],l[3]), Scalar(0,255,0), 2, LINE_AA);}
        */

    }




    imshow("Detected Lines (in red) - Standard Hough Line Transform", out_m);

    waitKey(0);


    //Image Load and noise remove
    /*****************************************************/
    //cv::GaussianBlur(img,img,Size(7,7),2,2);
    /*
    cv::cvtColor(img,gray,CV_BGR2GRAY);
    Mat dst,cdst,cdstP;
    // Edge detection
    Canny(gray, dst, 50, 200, 3);
    // Copy edges to the images that will display the results in BGR
    cvtColor(dst, cdst, COLOR_GRAY2BGR);
    cdstP = cdst.clone();
    // Standard Hough Line Transform
    vector<Vec2f> lines; // will hold the results of the detection
    HoughLines(dst, lines, 1, CV_PI/180, 150, 0, 0 ); // runs the actual detection
    // Draw the lines
    cout << "lines.size(): " << lines.size() << endl;
    for( size_t i = 0; i < lines.size(); i++ )
    {
       float rho = lines[i][0], theta = lines[i][1];
       Point pt1, pt2;
       double a = cos(theta), b = sin(theta);
       double x0 = a*rho, y0 = b*rho;
       pt1.x = cvRound(x0 + 1000*(-b));
       pt1.y = cvRound(y0 + 1000*(a));
       pt2.x = cvRound(x0 - 1000*(-b));
       pt2.y = cvRound(y0 - 1000*(a));
       line( cdst, pt1, pt2, Scalar(0,0,255), 3, LINE_AA);
    }
    // Probabilistic Line Transform
    vector<Vec4i> linesP; // will hold the results of the detection
    HoughLinesP(dst, linesP, 1, CV_PI/180, 50, 50, 10 ); // runs the actual detection
    // Draw the lines
    for( size_t i = 0; i < linesP.size(); i++ )
    {
       Vec4i l = linesP[i];
       line( cdstP, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0,0,255), 3, LINE_AA);
    }
    // Show results
    imshow("Source", img);
    imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst);
    imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP);
    waitKey(0);
    */

}


void MainWindow::on_pushButton_8_clicked()
{



    Mat Test = imread("C:/Users/tommy/Documents/build-ShapeAlignmentSystem-Desktop_Qt_5_12_11_MinGW_32_bit-Debug/Test Image/PanelEdge/PanelEdge/panel_edge2_2.bmp");


    double angle = 5;


    cv::Point2f center((Test.cols - 1) / 2.0, (Test.rows - 1) / 2.0);



    cv::Mat rot = cv::getRotationMatrix2D(center, angle, 1.0);

    cv::warpAffine(Test, Test, rot, Test.size());


    cv::imwrite("C:/Users/tommy/Documents/build-ShapeAlignmentSystem-Desktop_Qt_5_12_11_MinGW_32_bit-Debug/Test Image/PanelEdge/PanelEdge/hand_plus5.bmp",Test);


}


//1. Image Load
void MainWindow::on_pushButton_9_clicked()
{
    //Data Initialize
    if(!g_InImg1.empty())
    {
        g_InImg1.zeros(g_InImg1.rows, g_InImg1.cols, CV_8UC3);
    }
    if(!g_InImg2.empty())
    {
        g_InImg2.zeros(g_InImg2.rows, g_InImg2.cols, CV_8UC3);
    }

    //Iamge Load
    filename = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
    filename2 = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));


    QStringList left,right;
    auto left_a = filename.chopped(4);
    auto right_a = filename2.chopped(4);
    QString l = left_a + ".json";
    QString r = right_a + ".json";

    L_X_label=L_Y_label=R_X_label=R_Y_label=0;

    //Json
    QJsonObject body1, body2;
    QJsonDocument doc, doc_r;
    QFile file, file2;

    //Left
    file.setFileName(l); //File Read
    file.open(QIODevice::ReadOnly);
    QByteArray load_data = file.readAll();
    doc = QJsonDocument::fromJson(load_data);
    body1 = doc.object();
    QJsonArray s_array = body1.value("shapes").toArray();
    QJsonObject array_4 = s_array.at(3).toObject();
    QJsonArray array_4_point = array_4.value("points").toArray();
    QJsonDocument QJsonArray_conv;
    QJsonArray_conv.setArray(array_4_point);
    QString dataToString = QJsonArray_conv.toJson();
    std::string  t = dataToString.toUtf8().constData();
    std::cout << t << std::endl;

    char chars[] = "[] ";
    for(int i=0; i<strlen(chars); i++)
    {
        t.erase (std::remove(t.begin(), t.end(), chars[i]), t.end());
    }
    const char delim = ',';
    std::vector<std::string> out;
    tokenize(t, delim, out);

    cout << "L_x:" << std::stoi(out.at(0)) << ",L_y:" << std::stoi(out.at(1)) << endl;

    L_X_label = std::stoi(out.at(0));
    L_Y_label = std::stoi(out.at(1));



    //Right
    file2.setFileName(r); //File Read
    file2.open(QIODevice::ReadOnly);
    QByteArray load_data_r = file2.readAll();
    doc_r = QJsonDocument::fromJson(load_data_r);
    body2 = doc_r.object();
    QJsonArray s_array_r = body2.value("shapes").toArray();
    QJsonObject array_4_r = s_array_r.at(3).toObject();
    QJsonArray array_4_point_r = array_4_r.value("points").toArray();
    QJsonDocument QJsonArray_conv_r;
    QJsonArray_conv_r.setArray(array_4_point_r);
    QString dataToString_r = QJsonArray_conv_r.toJson();
    std::string  t2 = dataToString_r.toUtf8().constData();
    std::cout << t2 << std::endl;


    char chars_r[] = "[] ";
    for(int i=0; i<strlen(chars_r); i++)
    {
        t2.erase (std::remove(t2.begin(), t2.end(), chars_r[i]), t2.end());
    }
     const char delim2 = ',';
    std::vector<std::string> out2;
    tokenize(t2, delim2, out2);

    R_X_label = std::stoi(out2.at(0));
    R_Y_label = std::stoi(out2.at(1));

    file.close();
    file2.close();
    out.clear();
    out2.clear();




    g_InImg1 = cv::imread(filename.toStdString());
    g_InImg2 = cv::imread(filename2.toStdString());


    Mat nTemp = g_InImg1.clone();
    Mat nTemp2 = g_InImg2.clone();

    cv::resize(nTemp,nTemp,Size(),0.5,0.5,INTER_AREA);
    cv::resize(nTemp2,nTemp2,Size(),0.5,0.5,INTER_AREA);

    ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(nTemp.data,nTemp.cols,nTemp.rows,nTemp.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
    ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(nTemp2.data,nTemp2.cols,nTemp2.rows,nTemp2.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));



}


//2. find contour
void MainWindow::on_pushButton_10_clicked()
{

    //contour shape save check
    /*
    if(!bSavecont)
    {
        QMessageBox::information(this, "Save the shape error","Save the contour shape");
        return;
    }
     */

    //Data Initialize
    if(!g_InImg1_ROI.empty()){ g_InImg1_ROI.zeros(g_InImg1_ROI.rows, g_InImg1_ROI.cols, CV_8UC3);}
    if(!g_InImg2_ROI.empty()){ g_InImg2_ROI.zeros(g_InImg2_ROI.rows, g_InImg2_ROI.cols, CV_8UC3);}

    if(!L_hist_mat.empty()){ L_hist_mat.zeros(L_hist_mat.rows, L_hist_mat.cols, CV_8UC3);}
    if(!R_hist_mat.empty()){ R_hist_mat.zeros(R_hist_mat.rows, R_hist_mat.cols, CV_8UC3);}


    //ROI Setting
    cv::Mat ROI_L_g_InImg1 = g_InImg1(cv::Rect(0,0,1080,660)); //Left
    cv::Mat ROI_R_g_InImg1 = g_InImg2(cv::Rect(200,0,1080,660)); //Right


    g_InImg1_ROI = ROI_L_g_InImg1.clone();//Left
    g_InImg2_ROI = ROI_R_g_InImg1.clone();//Right

    //output for result
    //Left
    Mat outimg = ROI_L_g_InImg1.clone();
    g_Left_result=outimg.clone();

    //Right
    Mat outimg2 = ROI_R_g_InImg1.clone();
    g_Right_result=outimg2.clone();


    //Remove noise
    //Left
    Mat median_result;
    cv::medianBlur(ROI_L_g_InImg1,median_result,17);
    cv::GaussianBlur(median_result,median_result,Size(5,5),0,0);


    //Right
    Mat median_result2;
    cv::medianBlur(ROI_R_g_InImg1,median_result2,17);
    cv::GaussianBlur(median_result2,median_result2,Size(5,5),0,0);


    //shape match mat
    Mat shape_mat_left, shape_mat_right;
    shape_mat_left = median_result.clone();
    shape_mat_right = median_result2.clone();
    cv::cvtColor(shape_mat_left,shape_mat_left,CV_BGR2GRAY);
    cv::cvtColor(shape_mat_right,shape_mat_right,CV_BGR2GRAY);

    cv::threshold(shape_mat_left,shape_mat_left,0,255,THRESH_OTSU);
    cv::threshold(shape_mat_right,shape_mat_right,0,255,THRESH_OTSU);

    cv::imshow("shape_mat_left",shape_mat_left);
    cv::imshow("shape_mat_right",shape_mat_right);


    Mat Edge_Left, Edge_Right;
    Mat LX, LY, RX, RY;
    Canny_Ben(shape_mat_left,Edge_Left,70,130,3,0,LX,LY); //Get Edge
    Canny_Ben(shape_mat_right,Edge_Right,70,130,3,0,RX,RY); //Get Edge
    cv::imshow("Left",Edge_Left);
    cv::imshow("Right",Edge_Right);

    //Right
    Mat out_canny2;
    Canny_Ben(median_result2,out_canny2,70,130,3,0,R_SobelX_2,R_SobelY_2); //get the Gx, Gy
    R_SobelX_2.convertTo(R_SobelX_2,CV_64F);
    R_SobelY_2.convertTo(R_SobelY_2,CV_64F);


    //Left
    Mat out_canny;
    Canny_Ben(median_result,out_canny,70,130,3,0,L_SobelX_2,L_SobelY_2); //get the Gx, Gy
    L_SobelX_2.convertTo(L_SobelX_2,CV_64F);
    L_SobelY_2.convertTo(L_SobelY_2,CV_64F);




    //find contour
    //Left
    vector<vector<Point>> contours;
    vector<pair<double,int>> cont_are;
    vector<pair<double,int>> cont_simlar;
    vector<Vec4i> hierarchy1;

    //Right
    vector<vector<Point>> contours2;
    vector<pair<double,int>> cont_are2;
    vector<pair<double,int>> cont_simlar2;
    vector<Vec4i> hierarchy2;


    vector<double> left;
    vector<double> right;
    vector<vector<Point>> contours_l_chk;
    vector<vector<Point>> contours_r_chk;

    vector<vector<Point>> contours_filtered;
    vector<vector<Point>> contours2_filtered;

    Mat final_con = cv::Mat::zeros(outimg.rows, outimg.cols, CV_8UC1); //Mat create -> Initialize by '0'
    Mat final_con2 = cv::Mat::zeros(outimg.rows, outimg.cols, CV_8UC1); //Mat create -> Initialize by '0'



    int nLargeIdx,nLargeIdx2;

    if(contours.size() != 0) {contours.clear();}
    if(cont_are.size() != 0) {cont_are.clear();}
    if(g_contours_left.size() != 0) {g_contours_left.clear();}
    cv::findContours(Edge_Left, contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);

    if(contours2.size() != 0) {contours2.clear();}
    if(cont_are2.size() != 0) {cont_are2.clear();}
    if(g_contours_right.size() != 0) {g_contours_right.clear();}
    cv::findContours(Edge_Right, contours2, RETR_EXTERNAL, CHAIN_APPROX_NONE);


    //if not saved contour shape data,choose the long contour data
    if(!bSavecont)
    {
        Mat final_con = cv::Mat::zeros(outimg.rows, outimg.cols, CV_8UC1); //Mat create -> Initialize by '0'
        Mat final_con2 = cv::Mat::zeros(outimg2.rows, outimg2.cols, CV_8UC1); //Mat create -> Initialize by '0'
        //contour Length check
        for(int i=0; i<contours.size(); i++)
        {
            cont_are.push_back(make_pair(cv::arcLength(contours[i],false),i));
            cv::drawContours(final_con,contours,i,Scalar(255,255,255),5);
        }
        sort(cont_are.begin(),cont_are.end());
        nLargeIdx = cont_are.back().second;
      // cv::imshow("left_b",final_con);


        for(int i=0; i < contours[nLargeIdx].size(); i++)
        {
           g_contours_left.push_back(contours[nLargeIdx].at(i)); //Copy contour point data to global vector
        }
        Scalar c(255, 228, 0);
        if(bCntview)
        {
            cv::drawContours(outimg,contours,nLargeIdx,c,5);

        }
        else
        {
            cv::drawContours(outimg,contours,nLargeIdx,c,5);
        }




        //contour Length check
        for(int i=0; i<contours2.size(); i++)
        {
            cont_are2.push_back(make_pair(cv::arcLength(contours2[i],false),i));
            cv::drawContours(final_con2,contours2,i,Scalar(255,255,255),5);
        }
        sort(cont_are2.begin(),cont_are2.end());
        nLargeIdx2 = cont_are2.back().second;
       // cv::imshow("right_b",final_con2);



        for(int i=0; i < contours2[nLargeIdx2].size(); i++)
        {
           g_contours_right.push_back(contours2[nLargeIdx2].at(i)); //Copy contour point data to global vector
        }
        Scalar c2(255, 228, 0);
        if(bCntview)
        {
            cv::drawContours(outimg2,contours2,nLargeIdx2,c2,5);
        }
        else
        {
            cv::drawContours(outimg2,contours2,nLargeIdx2,c2,5);
        }
        //cv::imshow("left",final_con);
        //cv::imshow("right",final_con2);

        cont_are.clear();
        vector<pair<double,int>>().swap(cont_are);

        cont_are2.clear();
        vector<pair<double,int>>().swap(cont_are2);

    }

    else if(bSavecont)
    {


        cout << "Left contour size:" << contours.size() << endl;
        cout << "Right contour size:" << contours2.size() << endl;

            //Left
            if(contours.size() > 2) //abnoamal case. the other object on the image
            {
                //contour Length check


                for(int i=0; i<contours.size(); i++)
                {

                    //1. contour length check with saved shape contour,
                    /*
                    if( (cv::arcLength(contours[i],false) < cv::arcLength(g_contour_left_save,false)/2) || (cv::arcLength(contours[i],false) > cv::arcLength(g_contour_left_save,false)*2))
                    {
                        continue;
                    }
                    */

                            //probs[i] =  1.0 - fmin( matchShapes( contours[i], matchContour_, CV_CONTOURS_MATCH_I2, 0.0 ) / matchThreshold_, 1.0 );

                    //double prob = 1.0 - fmin( matchShapes(contours[i], g_contour_left_save, CV_CONTOURS_MATCH_I2, 0.0)/0.2, 1.0);


                    /*
                    Moments m_l = moments(contours[i],false);
                    cout << "m00:" << m_l.m00 << ",m01:" << m_l.m01 << ",m02:" << m_l.m02 << ",m03:" << m_l.m03 << ",m10:" << m_l.m10 << ",m11:" << m_l.m11 << ",m12:" << m_l.m12 <<",m20:" <<m_l.m20 << ",m21:" <<m_l.m21 <<",m30:"  << m_l.m30  << endl;

                    double h[7];
                    cv::HuMoments(m_l,h);
                    cout << "h0:" << h[0] << ",h1:" << h[1] << ",h2:" << h[2] << ",h3:" << h[3] << ",h4:" << h[4] << ",h5:" << h[5] << ",h6:" << h[6] << endl;
                    */

                    double prob = 1.0 - std::round(cv::matchShapes(g_contour_left_save,contours[i],CONTOURS_MATCH_I3,0) * 1000)/1000;
                    //QString s_prob = QString::number(prob);
                    //cout << "similar value: [" << i << "]index, value : [" << std::round(cv::matchShapes(g_contour_left_save,contours[i],CONTOURS_MATCH_I3,0) * 1000)/1000 << "]" << endl;
                    //cout << "similar value: [" << i << "]index, value : [" << s_prob << "]" << endl;

                    //cout << std::round(prob) << endl;

                    cont_simlar.push_back(make_pair(std::round(cv::matchShapes(g_contour_left_save,contours[i],CONTOURS_MATCH_I3,0) * 1000)/1000,i));
                    cv::drawContours(final_con,contours,i,Scalar(255,255,255),5);

                }
             //   cv::imshow("left_b",final_con);



                sort(cont_simlar.begin(), cont_simlar.end());
                //int left_n = cont_simlar.front().second;
                nLargeIdx = cont_simlar.front().second;
                cout << "Left final Index:" << nLargeIdx << endl;


                for(int i=0; i < contours[nLargeIdx].size(); i++)
                {
                   g_contours_left.push_back(contours[nLargeIdx].at(i)); //Copy contour point data to global vector
                }


                //cont_are.clear();
                //vector<pair<double,int>>().swap(cont_are);
                //contours.clear();
                //vector<vector<Point>>().swap(contours);



            }
            else if(contours.size() <= 2) //noamal case. the other object on the image
            {
                //contour Length check
                for(int i=0; i<contours.size(); i++)
                {
                    cont_are.push_back(make_pair(cv::arcLength(contours[i],false),i));
                    cv::drawContours(final_con,contours,i,Scalar(255,255,255),5);
                }
             //   cv::imshow("left_b",final_con);
                sort(cont_are.begin(),cont_are.end());
                nLargeIdx = cont_are.back().second;

                for(int i=0; i < contours[nLargeIdx].size(); i++)
                {
                   g_contours_left.push_back(contours[nLargeIdx].at(i)); //Copy contour point data to global vector
                }
            }


            //Right
            if(contours2.size() > 2) //abnoamal case. the other object on the image
            {





                //contour Length check
                for(int i=0; i<contours2.size(); i++)
                {


                    Moments m_r = moments(contours2[i],false);
                    //cout << "m00_r:" << m_r.m00 << ",m01_r:" << m_r.m01 << ",m02_r:" << m_r.m02 << ",m03_r:" << m_r.m03 << ",m10_r:" << m_r.m10 << ",m11_r:" << m_r.m11 << ",m12_r:" << m_r.m12 <<",m20_r:" <<m_r.m20 << ",m21_r:" <<m_r.m21 <<",m30_r:"  << m_r.m30  << endl;

                    double h_r[7];
                    cv::HuMoments(m_r,h_r);
                    //cout << "h0_r:" << h_r[0] << ",h1_r:" << h_r[1] << ",h2_r:" << h_r[2] << ",h3_r:" << h_r[3] << ",h4_r:" << h_r[4] << ",h5_r:" << h_r[5] << ",h6_r:" << h_r[6] << endl;





                    //1. contour length check with saved shape contour,
                    /*
                    if( (cv::arcLength(contours2[i],false) < cv::arcLength(g_contour_right_save,false)/2) || (cv::arcLength(contours2[i],false) > cv::arcLength(g_contour_right_save,false)*2))
                    {
                        continue;
                    }
                    */
                    //double prob = 1.0 - fmin( matchShapes(contours2[i], g_contour_right_save, CV_CONTOURS_MATCH_I2, 0.0)/0.2, 1.0);
                    double prob = std::round(cv::matchShapes(g_contour_right_save,contours2[i],CONTOURS_MATCH_I3,0) * 1000)/1000;
                    //cout << "similar value_right: [" << i << "]index, value : [" << std::round(cv::matchShapes(g_contour_right_save,contours2[i],CONTOURS_MATCH_I3,0) * 1000)/1000 << "]" << endl;
                    //cout << "similar value_right: [" << i << "]index, value : [" << prob << "]" << endl;

                    //cout << std::round(prob) << endl;

                    cont_simlar2.push_back(make_pair(std::round(cv::matchShapes(g_contour_right_save,contours2[i],CONTOURS_MATCH_I3,0)*1000)/1000,i));
                    cv::drawContours(final_con2,contours2,i,Scalar(255,255,255),5);

                }
              //  cv::imshow("right_b",final_con2);
                int nLargeIdx2 = 0;
                if(cont_simlar2.size()>1)
                {
                    sort(cont_simlar2.begin(), cont_simlar2.end());
                    nLargeIdx2 = cont_simlar2.front().second;
                }

                //int left_n = cont_simlar.end().second;

                //cout << "Right final Index:" << nLargeIdx2 << endl;



                for(int i=0; i < contours2[nLargeIdx2].size(); i++)
                {
                   g_contours_right.push_back(contours2[nLargeIdx2].at(i));
                }
            }
            else if(contours2.size() <= 2) //noamal case. the other object on the image
            {
                //contour Length check
                for(int i=0; i<contours2.size(); i++)
                {
                    cont_are2.push_back(make_pair(cv::arcLength(contours2[i],false),i));
                    cv::drawContours(final_con2,contours2,i,Scalar(255,255,255),5);
                }
                //cv::imshow("right_b",final_con2);
                sort(cont_are2.begin(),cont_are2.end());
                nLargeIdx2 = cont_are2.back().second;

                for(int i=0; i < contours2[nLargeIdx2].size(); i++)
                {
                   g_contours_right.push_back(contours2[nLargeIdx2].at(i)); //Copy contour point data to global vector
                }
            }


            contours_l_chk.push_back(g_contours_left);
            contours_r_chk.push_back(g_contours_right);



           Scalar c(255, 228, 0);


           if(bCntview)
           {
               cv::drawContours(outimg,contours_l_chk,0,c,5);
               cv::drawContours(outimg2,contours_r_chk,0,c,5);
           }
           else
           {
               cv::drawContours(outimg,contours_l_chk,0,c,5);
               cv::drawContours(outimg2,contours_r_chk,0,c,5);
           }

           //cv::imshow("left_f",outimg);
           //cv::imshow("right_f",outimg2);







    }

    //Left
    /****************************************************************************************************/

    g_L_index = nLargeIdx;
    g_L_contours.assign(contours.begin(), contours.end()); //real contour(contoru를 draw하기 위한 데이터)
    //contour coordinate duplicate point remove
    removeduplpt(g_contours_left);


    //data_Left_mag, data_Left_ang Points order work
    //반시계방향. (Reference Point : (0,0), Calculation Point : Contour Point)
    vector<tuple<float, int, int>> order_pts;

    for(int i=0; i<g_contours_left.size(); i++)
    {
        Point Ref = Point(0,0);
        int x = g_contours_left.at(i).x;
        int y = g_contours_left.at(i).y;
        Point cal = Point(x,y);

        float temp = atan2(cal.y - Ref.y, cal.x - Ref.x);
        temp = temp * (180.0/CV_PI);//Radian -> degree
        if (temp < 0.0) { //convert to -pi ~ +pi ---> 0~2pi
            temp += 360.0;
        }

        order_pts.push_back(make_tuple(temp,x,y));
    }

    sort(order_pts.begin(), order_pts.end()); //order contorur points by Angle
    g_contours_left.clear();

    //Reallocate the contour points by ordered data
    for(int i=0; i<order_pts.size(); i++)
    {
        int x = std::get<1>(order_pts.at(i));
        int y = std::get<2>(order_pts.at(i));
        Point temp = Point(x,y);
        g_contours_left.push_back(temp);

    }
    g_contours_left_back.assign(g_contours_left.begin(), g_contours_left.end());
    /****************************************************************************************************/

    //Right
    /****************************************************************************************************/

    g_R_index = nLargeIdx2;
    g_R_contours.assign(contours2.begin(), contours2.end()); //real contour(contoru를 draw하기 위한 데이터)
    removeduplpt(g_contours_right);

    //시계방향. (Reference Point : (0,0), Calculation Point : Contour Point)
    vector<tuple<float, int, int>> order_pts2;

    for(int i=0; i<g_contours_right.size(); i++)
    {
        Point Ref = Point(540,0);
        int x = g_contours_right.at(i).x;
        int y = g_contours_right.at(i).y;
        Point cal = Point(x,y);

        float temp = atan2(cal.y - Ref.y, Ref.x - cal.x);
        temp = temp * (180.0/CV_PI);//Radian -> degree
        if (temp < 0.0) { //convert to -pi ~ +pi ---> 0~2pi
            temp += 360.0;
        }

        order_pts2.push_back(make_tuple(temp,x,y));
    }

    sort(order_pts2.begin(), order_pts2.end()); //order contorur points by Angle
    g_contours_right.clear();

    //Reallocate the contour points by ordered data
    for(int i=0; i<order_pts2.size(); i++)
    {
        int x = std::get<1>(order_pts2.at(i));
        int y = std::get<2>(order_pts2.at(i));
        Point temp = Point(x,y);
        g_contours_right.push_back(temp);

    }
    g_contours_right_back.assign(g_contours_right.begin(), g_contours_right.end());

    /****************************************************************************************************/

    ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(outimg.data,outimg.cols,outimg.rows,outimg.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
    ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(outimg2.data,outimg2.cols,outimg2.rows,outimg2.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));

}

//3. Get the normal direction angle and magnitude
void MainWindow::on_pushButton_11_clicked()
{

    //data null chaeck
    if(data_Left_mag.size() != 0) {data_Left_mag.clear();}
    if(data_Left_ang.size() != 0) {data_Left_ang.clear();}
    if(data_Left_mag_dev.size() != 0) {data_Left_mag_dev.clear();}
    if(data_Left_ang_dev.size() != 0) {data_Left_ang_dev.clear();}

    if(data_Right_mag.size() != 0) {data_Right_mag.clear();}
    if(data_Right_ang.size() != 0) {data_Right_ang.clear();}
    if(data_Right_mag_dev.size() != 0) {data_Right_mag_dev.clear();}
    if(data_Right_ang_dev.size() != 0) {data_Right_ang_dev.clear();}

    if(Left_gx.size() != 0) {Left_gx.clear();}
    if(Left_gy.size() != 0) {Left_gy.clear();}
    if(Right_gx.size() != 0) {Right_gx.clear();}
    if(Right_gy.size() != 0) {Right_gy.clear();}



    if(Left_gradient.size() != 0) {Left_gradient.clear();}
    if(Right_gradient.size() != 0) {Right_gradient.clear();}


    if(qv_x.size() != 0){qv_x.clear();}
    if(qv_x2.size() != 0){qv_x2.clear();}
    if(qv_x3.size() != 0){qv_x3.clear();}
    if(qv_x4.size() != 0){qv_x4.clear();}

    if(qv_y.size() != 0){qv_y.clear();}
    if(qv_y2.size() != 0){qv_y2.clear();}
    if(qv_y3.size() != 0){qv_y3.clear();}
    if(qv_y4.size() != 0){qv_y4.clear();}
    if(qv_y5.size() != 0){qv_y5.clear();}


    //Left
    vector<tuple<float, int, int>> data_Left_ang_dev_local;
    vector<tuple<float, int, int>> data_Left_mag_dev_local;
    Mat Grad_Left = g_InImg1_ROI.clone();
    cvtColor(Grad_Left,Grad_Left,CV_BGR2GRAY);


    //Right
    vector<tuple<float, int, int>> data_Right_ang_dev_local;
    vector<tuple<float, int, int>> data_Right_mag_dev_local;
    Mat Grad_Right = g_InImg2_ROI.clone();
    cvtColor(Grad_Right,Grad_Right,CV_BGR2GRAY);
    cv::medianBlur(Grad_Right,Grad_Right,3);


    //Calculate angle, magnitude
    //Left
    //////////////////////////////////////////////////////////////////////////////////////////////////////////
     for(int i=1; i<g_contours_left.size()-1; i++)
     {

         int xCoor = g_contours_left.at(i).x;
         int yCoor = g_contours_left.at(i).y;

         //Magnitude
         float l_mag_x = L_SobelX_2.at<double>(yCoor,xCoor);
         float l_mag_y = L_SobelY_2.at<double>(yCoor,xCoor);
         float l_mag = sqrt(pow(l_mag_x,2) + pow(l_mag_y,2));



         l_mag_x = abs(l_mag_x);
         l_mag_y = abs(l_mag_y);


         Left_gx.push_back(make_tuple(l_mag_x,xCoor,yCoor));
         Left_gy.push_back(make_tuple(l_mag_y,xCoor,yCoor));


         //Angle
         //float temp = atan2(l_mag_y,l_mag_x);
         float temp = atan2(l_mag_y,l_mag_x);
         temp = temp * (180.0/CV_PI);//Radian -> degree
         if (temp < 0.0) { //convert to -pi ~ +pi ---> 0~2pi
             temp += 360.0;
         }

         data_Left_mag.push_back(make_tuple(l_mag,xCoor,yCoor));
         data_Left_ang.push_back(make_tuple(temp,xCoor,yCoor));

         if(i==1)
         {
             std::string tmp = std::to_string(i);
             char const *num_text = tmp.c_str();

             cv::putText(g_Left_result, num_text, Point(xCoor,yCoor),FONT_HERSHEY_PLAIN,1,Scalar(255,0,0),1);
             cv::line(g_Left_result,Point(xCoor,yCoor),Point(xCoor,yCoor),Scalar(197,65,217),5,LINE_AA);

         }
         else if((i % 101)==0)
         {
             std::string tmp = std::to_string(i);
             char const *num_text = tmp.c_str();

             cv::putText(g_Left_result, num_text, Point(xCoor,yCoor),FONT_HERSHEY_PLAIN,1,Scalar(255,0,0),1);
             cv::line(g_Left_result,Point(xCoor,yCoor),Point(xCoor,yCoor),Scalar(0,94,255),3,LINE_AA);

         }



     }


     //////////////////////////////////////////////////////////////////////////////////////////////////////////
     //Right
     //////////////////////////////////////////////////////////////////////////////////////////////////////////
      for(int i=1; i<g_contours_right.size()-1; i++)
      {

          int xCoor = g_contours_right.at(i).x;
          int yCoor = g_contours_right.at(i).y;

          //Magnitude
          float r_mag_x = R_SobelX_2.at<double>(yCoor,xCoor);
          float r_mag_y = R_SobelY_2.at<double>(yCoor,xCoor);
          float r_mag = sqrt(pow(r_mag_x,2) + pow(r_mag_y,2));


          r_mag_x = abs(r_mag_x);
          r_mag_y = abs(r_mag_y);


          Right_gx.push_back(make_tuple(r_mag_x,xCoor,yCoor));
          Right_gy.push_back(make_tuple(r_mag_y,xCoor,yCoor));




          //Angle
          float temp = atan2(r_mag_y,r_mag_x);
          temp = temp * (180.0/CV_PI);//Radian -> degree
          if (temp < 0.0) { //convert to -pi ~ +pi ---> 0~2pi
              temp += 360.0;
          }



          data_Right_mag.push_back(make_tuple(r_mag,xCoor,yCoor));
          data_Right_ang.push_back(make_tuple(temp,xCoor,yCoor));

          if(i==1)
          {
              std::string tmp = std::to_string(i);
              char const *num_text = tmp.c_str();

              cv::putText(g_Right_result, num_text, Point(xCoor,yCoor),FONT_HERSHEY_PLAIN,1,Scalar(255,0,0),1);
              cv::line(g_Right_result,Point(xCoor,yCoor),Point(xCoor,yCoor),Scalar(197,65,217),5,LINE_AA);

          }
          else if((i % 101)==0)
          {
              std::string tmp = std::to_string(i);
              char const *num_text = tmp.c_str();

              cv::putText(g_Right_result, num_text, Point(xCoor,yCoor),FONT_HERSHEY_PLAIN,1,Scalar(255,0,0),1);
              cv::line(g_Right_result,Point(xCoor,yCoor),Point(xCoor,yCoor),Scalar(0,94,255),3,LINE_AA);

          }



      }


     //////////////////////////////////////////////////////////////////////////////////////////////////////////
     // Extreme point cal Left_gradient
     for(int i=0; i<Left_gx.size(); i++)
     {
         float left_gx = std::get<0>(Left_gx.at(i)); //gx
         float left_gy = std::get<0>(Left_gy.at(i)); //gy
         float temp = DIFF_ABS(fabs(left_gx),fabs(left_gy));
         Left_gradient.push_back(make_tuple(temp, std::get<1>(Left_gx.at(i)), std::get<2>(Left_gx.at(i))));

     }


     sort(Left_gradient.begin(), Left_gradient.end());

     ExtremePoint.x = std::get<1>(Left_gradient.front());
     ExtremePoint.y = std::get<2>(Left_gradient.front());


     for(int i=0; i<Right_gx.size(); i++)
     {

         float right_gx = std::get<0>(Right_gx.at(i)); //gx
         float right_gy = std::get<0>(Right_gy.at(i)); //gy
         float temp = DIFF_ABS(fabs(right_gx),fabs(right_gy));
         Right_gradient.push_back(make_tuple(temp, std::get<1>(Right_gx.at(i)), std::get<2>(Right_gy.at(i))));

     }

     sort(Right_gradient.begin(), Right_gradient.end());

     ExtremePoint2.x = std::get<1>(Right_gradient.front());
     ExtremePoint2.y = std::get<2>(Right_gradient.front());





     //draw contour
     Scalar c(255, 0, 0);
     if(bCntview)
     {
         cv::drawContours(g_Left_result,g_L_contours,g_L_index,c,5);
         cv::drawContours(g_Right_result,g_R_contours,g_R_index,c,5);
     }
     else
     {
         cv::drawContours(g_Left_result,g_L_contours,g_L_index,c,0);
         cv::drawContours(g_Right_result,g_R_contours,g_R_index,c,0);
     }


     cv::drawMarker(g_Left_result,ExtremePoint,Scalar(0,255,0),MARKER_TILTED_CROSS,12,7,8);
     cv::drawMarker(g_Right_result,ExtremePoint2,Scalar(0,255,0),MARKER_TILTED_CROSS,12,7,8);

     //Ground Truth (Label Data)
     cv::Point Left_ground, Right_ground;

     Left_ground.x = L_X_label;
     Left_ground.y = L_Y_label;
     Right_ground.x = R_X_label-200; //because of crop image
     Right_ground.y = R_Y_label;

     cout << "Get Gradient Step" << endl;
     cout << "Left_ground_x:"<< L_X_label << endl;
     cout << "Left_ground_y:"<< L_Y_label << endl;

     cv::drawMarker(g_Left_result,Left_ground,Scalar(0,0,255),MARKER_SQUARE,6,7,8);
     cv::drawMarker(g_Right_result,Right_ground,Scalar(0,0,255),MARKER_SQUARE,6,7,8);






     //Detection Position
     ui->Left_x_detect->setText(QString::number(ExtremePoint.x));
     ui->Left_y_detect->setText(QString::number(ExtremePoint.y));
     ui->Right_x_detect->setText(QString::number(ExtremePoint2.x+200));
     ui->Right_y_detect->setText(QString::number(ExtremePoint2.y));

     //G.T. Position
     ui->Left_x_GT->setText(QString::number(Left_ground.x));
     ui->Left_y_GT->setText(QString::number(Left_ground.y));
     ui->Right_x_GT->setText(QString::number(Right_ground.x));
     ui->Right_y_GT->setText(QString::number(Right_ground.y));

     //Different Detection Position <-> G.T.
     double x_diff_left = DIFF_ABS(ExtremePoint.x, Left_ground.x);
     double y_diff_left = DIFF_ABS(ExtremePoint.y, Left_ground.y);
     double x_diff_right = DIFF_ABS(ExtremePoint2.x, Right_ground.x);
     double y_diff_right = DIFF_ABS(ExtremePoint2.y, Right_ground.y);

     ui->diff_x_left->setText(QString::number(x_diff_left));
     ui->diff_y_left->setText(QString::number(y_diff_left));
     ui->diff_x_right->setText(QString::number(x_diff_right));
     ui->diff_y_right->setText(QString::number(y_diff_right));







     ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(g_Left_result.data,g_Left_result.cols,g_Left_result.rows,g_Left_result.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
     ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(g_Right_result.data,g_Right_result.cols,g_Right_result.rows,g_Right_result.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));




}

void MainWindow::showPopup() //show the pop-up
{


}


//Magnitude data
void MainWindow::on_pushButton_12_clicked()
{
    dlg = new SecDialog;
    connect(this,SIGNAL(Send1(std::vector<std::tuple<float, int, int>>)),dlg, SLOT(Recv_value_mag(std::vector<std::tuple<float, int, int>>)));
    emit Send1(data_Left_mag);
    dlg->setModal(true);
    dlg->exec();
}

//Magnitude, angle data graph oputput
void MainWindow::on_pushButton_13_clicked()
{
    add_data();
    plot_graph();

}

//Magnitude_smooth
void MainWindow::on_pushButton_14_clicked()
{
    dlg = new SecDialog;
    connect(this,SIGNAL(Send1(std::vector<std::tuple<float, int, int>>)),dlg, SLOT(Recv_value_mag_smooth(std::vector<std::tuple<float, int, int>>)));
    emit Send1(data_Left_mag_smooth);
    dlg->setModal(true);
    dlg->exec();
}

//Angle_smooth
void MainWindow::on_pushButton_15_clicked()
{
    dlg = new SecDialog;
    connect(this,SIGNAL(Send1(std::vector<std::tuple<float, int, int>>)),dlg, SLOT(Recv_value_ang_smooth(std::vector<std::tuple<float, int, int>>)));
    emit Send1(data_Left_ang_smooth);
    dlg->setModal(true);
    dlg->exec();
}



//mag dev
void MainWindow::on_pushButton_16_clicked()
{
    dlg = new SecDialog;
    connect(this,SIGNAL(Send1(std::vector<std::tuple<float, int, int>>)),dlg, SLOT(Recv_value_dev_mag(std::vector<std::tuple<float, int, int>>)));
    emit Send1(data_Left_mag_dev);
    dlg->setModal(true);
    dlg->exec();
}

//ang dev
void MainWindow::on_pushButton_17_clicked()
{
    dlg = new SecDialog;
    connect(this,SIGNAL(Send1(std::vector<std::tuple<float, int, int>>)),dlg, SLOT(Recv_value_dev_ang(std::vector<std::tuple<float, int, int>>)));
    emit Send1(data_Left_ang_dev);
    dlg->setModal(true);
    dlg->exec();
}


void MainWindow::on_pushButton_18_clicked()
{
    //1. Iamge Load
    QString filename = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
    Mat InImg1 = cv::imread(filename.toStdString(),IMREAD_GRAYSCALE);
    cv::Mat ROI_L_g_InImg1 = InImg1(cv::Rect(0,0,1080,830)); //ROI Setting
    cv::resize(ROI_L_g_InImg1,ROI_L_g_InImg1,Size(),0.5,0.5,INTER_AREA);



    //2. Remove noise
    Mat median_result;
    cv::medianBlur(ROI_L_g_InImg1,median_result,3);
 //   cv::imshow("median",median_result);

    // contrast process, binary convert parameter by Light value
    // 1) Light value 30 : contrast thres 45, binary thres 35
    // 2) Light value 50 : contrast thres 65, binary thres 80
    // 3) Light value 100 : contrast thres 100, binary thres 110
    // 4) Light value 150 : contrast thres 125, binary thres 155
    // 5) Light value 200 : contrast thres 190, binary thres 200
    // 6) Light value 255 : contrast thres 230, binary thres 245



    //3. contrast process
    float alpha = 1.5f;
    Mat contpre = median_result + (median_result - 65) * alpha;
 //   cv::imshow("Contrast_Processing",contpre);


    //4. Threshold
    cv::threshold(median_result,median_result,80,255,THRESH_BINARY);
  //  cv::imshow("InputImage_Left",median_result);



    //3. canny
    Mat out_canny;
    cv::Canny(median_result,out_canny,70,130);
  //  cv::imshow("canny",out_canny);


}

//중복 Point제거 위해 사용
void MainWindow::removeduplpt(std::vector<cv::Point>& vec)
{
    std::unordered_set<cv::Point> pointset; //STL dataconatiner

    auto itor = vec.begin();
    while(itor != vec.end())
    {
        //check duplicate the hash data
        if(pointset.find(*itor) != pointset.end())
        {
            itor = vec.erase(itor);
        }
        else
        {
            pointset.insert(*itor);
            itor++;
        }
    }
}

void MainWindow::radio_button_left()
{
    bchoose_graph = false;
}
void MainWindow::radio_button_right()
{
    bchoose_graph = true;
}

void MainWindow::on_checkBox_stateChanged(int arg1)
{
    //no event
    //chekc ar1 = 2
    if(arg1 == 2)
    {
        bCntview = true;
        this->ui->checkBox->setText(QString("Visible"));
    }

    //uncheck ar1 = 0
    else if(arg1 == 0)
    {
        bCntview = false;
        this->ui->checkBox->setText(QString("UnVisible"));
    }

}


void MainWindow::on_pushButton_19_clicked()
{
    //Left, Right Contour Shape Save
    if((g_contours_left.empty() || g_contours_right.empty()) && (!bSavecont))
    {
        QMessageBox::information(this, "Save the shape error","Do the 1time detect extreme point");
        return;
    }

    if((!g_contour_left_save.empty()||!g_contour_right_save.empty()) &&  bSavecont)
    {
        QMessageBox::information(this, "Save the shape error","Aleady Saved Shape Data");
        return;
    }

    bSavecont = true;
    g_contour_left_save.assign(g_contours_left.begin(),g_contours_left.end());
    g_contour_right_save.assign(g_contours_right.begin(),g_contours_right.end());


}

void MainWindow::tokenize(std::string const &str, const char delim, std::vector<std::string> &out)
{
    size_t start;
    size_t end = 0;

    while ((start = str.find_first_not_of(delim, end)) != std::string::npos)
    {
        end = str.find(delim, start);
        out.push_back(str.substr(start, end - start));
    }
}


void MainWindow::on_pushButton_20_clicked()
{

    QStringList strFilters;
    strFilters += "*.png";

    QDirIterator it("C:/Test Image_20210913",strFilters,QDir::Files | QDir::NoSymLinks , QDirIterator::Subdirectories);
    while(it.hasNext())
    {
        qDebug() << it.next();

    }
}

