//#include "mainwindow.h"

//#include "ui_mainwindow.h"

//#define DIFF_ABS(X,Y) ((X)>(Y)? (X)-(Y) : (Y)-(X))

////QT_CHARTS_USE_NAMESPACE

////struct myclass_judge_x_coordinate{
////    bool operator() (cv::Point pt1, cv::Point pt2) {return (pt1.x < pt2.x);}
////}myobject_x_extern_m;


////struct myclass_judge_y_coordinate{
////    bool operator() (cv::Point pt1, cv::Point pt2) {return (pt1.y < pt2.y);}
////}myobject_y_extern_m;

//////중복 Point 제거 위해 사용
////bool operator==(const cv::Point& pt1, const cv::Point& pt2)
////{
////    return ((pt1.x == pt2.x) && (pt1.y == pt2.y));
////}

////namespace std
////{
////    template<>
////    struct hash<cv::Point> //std hash function overriding
////    {
////        size_t operator()(cv::Point const& pt) const
////        {
////            return (size_t)(pt.x*100 + pt.y); //make hash data
////        }
////    };
////}

////using namespace std;
////using namespace cv;

//MainWindow* ui_ext = NULL;

////Thread Object Create
////QThread* thread_Align = new QThread;
////QThread* thread_PLC = new QThread;
////AlignProcess* worker_Align = new AlignProcess();
////PLCComProcess* worker_PLC = new PLCComProcess();
////VirtualPointDetection* test = new VirtualPointDetection();
////Drawgraph* dl_new = new Drawgraph();

////Timer Create
////shared_ptr<QTimer> m_pTimer;
////shared_ptr<QTimer> m_CaliTimer; //Calibration Timer


////************************************************//
////Gradient Based method variable
//Mat g_InImg1, g_InImg2, g_InImg1_ROI, g_InImg2_ROI, dst1, dst2;
//vector<Point> g_contours_left, g_contours_right;
//vector<Point> g_contours_left_back, g_contours_right_back; //최종적으로 찾은 Extreme point에서 FineTune(for round extrem point)
//vector<Point> g_contour_left_save, g_contour_right_save; //contour shape compare 변수 (기준데이터)
//bool bSavecont; //constour shape 저장 여부 확인변수

////test result mat
//Mat g_Left_result, g_Right_result;
//vector<vector<Point>> g_L_contours, g_R_contours;
//int g_L_index, g_R_index;

//QString filename;
//QString filename2;



////Left
///************************************************************************/
////Angle, Dev
//vector<tuple<float, int, int>> data_Left_ang;
//vector<tuple<float, int, int>> data_Left_mag;
//vector<tuple<float, int, int>> data_Left_ang_smooth;
//vector<tuple<float, int, int>> data_Left_mag_smooth;
////Deviation
//vector<tuple<float, int, int>> data_Left_ang_dev;
//vector<tuple<float, int, int>> data_Left_mag_dev;

//vector<tuple<float, int, int>> Left_gx;
//vector<tuple<float, int, int>> Left_gy;
//vector<tuple<float, int, int>> Left_gradient;

//vector<tuple<float, int, int>> Right_gx;
//vector<tuple<float, int, int>> Right_gy;
//vector<tuple<float, int, int>> Right_gradient;
///************************************************************************/
////Right
///************************************************************************/
////Angle, Dev
//vector<tuple<float, int, int>> data_Right_ang;
//vector<tuple<float, int, int>> data_Right_mag;
//vector<tuple<float, int, int>> data_Right_ang_smooth;
//vector<tuple<float, int, int>> data_Right_mag_smooth;
////Deviation
//vector<tuple<float, int, int>> data_Right_ang_dev;
//vector<tuple<float, int, int>> data_Right_mag_dev;
///************************************************************************/

///***********************************************************************/
////Sobel operation for angle, magnitude
////Left
//Mat L_SobelX_2, L_SobelY_2;

////Right
//Mat R_SobelX_2, R_SobelY_2;
///***********************************************************************/


///***********************************************************************/
////Label Data Variable
//int L_X_label, L_Y_label, R_X_label, R_Y_label;

///***********************************************************************/




////Select visible contour
//bool bCntview = false;

////Histrogram equalization mat (use at the gradeint)
//Mat L_hist_mat, R_hist_mat;

////Input Mat variable
//Mat img, img2;
//Mat img_clone, img2_clone; //최종ExtremePoint Save용

////gradient Mat Copy
//Mat L_grad_cpy,R_grad_cpy;

////Roation Test flag
//bool bTestRot=false;

////variable
//int repaint_test_var=0;
//float L_angle[640][480], R_angle[640][480], L_mag[640][480], R_mag[640][480] = {0.0f};
//float dst_angle_left[640][480]= {0.0f};
//float dst_angle_right[640][480]= {0.0f};
//float dst_angle_left_derv[640][480]= {0.0f};
//Point ExtremePoint,ExtremePoint2;
//vector<vector<Point>> contours_left_new;


////Mat for Houghline Test
//Mat TestHough;

//MainWindow::MainWindow(QWidget *parent):
//    QMainWindow(parent)
//    , ui(new Ui::MainWindow)
//{
//    ui->setupUi(this);
//    ui->pushButton_2->setVisible(false);
//    ui->btn_median->setVisible(false);
//    ui->pushButton_4->setVisible(false);
//    ui->pushButton_3->setVisible(false);


//    ui->pushButton_2->setVisible(false);
//    ui->btn_median->setVisible(false);
//    ui->pushButton_4->setVisible(false);
//    ui->pushButton_3->setVisible(false);
//    ui->pushButton_5->setVisible(false);
//    ui->groupBox_7->setVisible(false);
//    ui->pushButton->setVisible(false);
//    ui->pushButton_6->setVisible(false);
//    ui->bRotationUse->setVisible(false);
//    ui->edttestangle->setVisible(false);
//    ui->btnRotation->setVisible(false);
//    ui->pushButton_18->setVisible(false);
//    ui->label_17->setVisible(false);
//    ui->label_16->setVisible(false);
//    ui->label_18->setVisible(false);
//    ui->pushButton_8->setVisible(false);
//    ui->pushButton_7->setVisible(false);

//    ui->pushButton_17->setVisible(false);
//    ui->pushButton_12->setVisible(false);
//    ui->pushButton_16->setVisible(false);
//    ui->pushButton_14->setVisible(false);
//    ui->pushButton_15->setVisible(false);

//    ui_ext = this;
////    bThreadStatus = false;
//    bchoose_graph = false;
//    bSavecont = false;

//    //#1 graph screen
//    //graph1 gx blue
//    ui->widget->addGraph();
//    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);
//    ui->widget->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
//    //graph2 gy Red
//    ui->widget->addGraph();
//    ui->widget->graph(1)->setLineStyle(QCPGraph::lsLine);
//    ui->widget->graph(1)->setPen(QPen(QColor(255, 0, 0), 2));

//    ui->widget->xAxis->setLabel("Index");
//    if(bchoose_graph)
//    {
//        ui->widget->yAxis->setLabel("Gx,Gy[Right]]");
//    }
//    else
//    {
//        ui->widget->yAxis->setLabel("Gx,Gy[Left]]]");
//    }

//    ui->widget->xAxis->rescale(false);
//    ui->widget->yAxis->rescale(false);



//    //#2 graph screen
//    //graph1 angle blue
//    ui->widget_2->addGraph();
//    ui->widget_2->graph(0)->setLineStyle(QCPGraph::lsLine);
//    ui->widget_2->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
//    ui->widget_2->xAxis->setLabel("Index");
//    //ui->widget_2->yAxis->setLabel("Angle[Left]");
//    if(bchoose_graph)
//    {
//        ui->widget_2->yAxis->setLabel("Angle[Right]");
//    }
//    else
//    {
//        ui->widget_2->yAxis->setLabel("Angle[Left]");
//    }
//    ui->widget_2->xAxis->rescale(false);
//    ui->widget_2->yAxis->rescale(false);
//    //ui->widget_2->replot();

//    //#3 graph screen
//    //graph1 gx blue
//    ui->widget_3->addGraph();
//    ui->widget_3->graph(0)->setLineStyle(QCPGraph::lsLine);
//    ui->widget_3->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
//    ui->widget_3->xAxis->setLabel("Index");
//    //ui->widget_3->yAxis->setLabel("Magnitude[Left]");
//    if(bchoose_graph)
//    {
//        ui->widget_3->yAxis->setLabel("Magnitude[Right]]");
//    }
//    else
//    {
//        ui->widget_3->yAxis->setLabel("Magnitude[Left]");
//    }
//    ui->widget_3->xAxis->rescale(false);
//    ui->widget_3->yAxis->rescale(false);



//}

//MainWindow::~MainWindow()
//{
//    delete ui;
//}

#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////// Tsung-Pao Cheng //////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

Mat left_image, right_image;
Mat left_smooth_image, right_smooth_image;
vector<Point> left_image_contour, right_image_contour;
Mat left_contour_image, right_contour_image;

vector<tuple<double, double>> left_image_Gradient, right_image_Gradient;
tuple<vector<double>, vector<double>> left_image_result, right_image_result;

tuple<int, int> left_image_groundTruth, right_image_groundTruth;

//1. Image Load
void MainWindow::on_Image_Load_Button_clicked()
{
//    test_all_data();

    //Iamge Load
    QString left_image_path = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
    QString right_image_path = QFileDialog::getOpenFileName(this,tr("Choose"),"",tr("Images (*.png *.jpg *.jpeg *.bmp *.gif)"));
    cout << ui->radioButton->isChecked() << endl;

    if(left_image_path.toStdString() == "" or right_image_path.toStdString() == ""){
        return;
    }

    left_image_groundTruth = readJsonFile(left_image_path.chopped(4) + ".json");
    right_image_groundTruth = readJsonFile(right_image_path.chopped(4) + ".json");

//    left_image_groundTruth = make_tuple(0, 0);
//    right_image_groundTruth = make_tuple(0, 0);

    Image_Load(left_image_path.toStdString(), left_image);
    Image_Load(right_image_path.toStdString(), right_image);
//    getExtremePoint(left_image_path.toStdString(), 'L', true);

    Mat show_left_image = left_image.clone();
    Mat show_right_image = right_image.clone();

//    resize(show_left_image,show_left_image,Size(),0.5,0.5,INTER_AREA);
//    resize(show_right_image,show_right_image,Size(),0.5,0.5,INTER_AREA);

//    ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(show_left_image.data, show_left_image.cols, show_left_image.rows, show_left_image.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
//    ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(show_right_image.data, show_right_image.cols, show_right_image.rows, show_right_image.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));
}


//2. find contour
void MainWindow::on_Find_Contour_Button_clicked()
{
    vector<Vec4i> leftBestTwoLines, rightBestTwoLines;

    Find_Contour_Button(left_image, left_smooth_image, left_image_contour, leftBestTwoLines, 'L');
    Find_Contour_Button(right_image, right_smooth_image, right_image_contour, rightBestTwoLines, 'R');

    left_contour_image = left_smooth_image.clone();
    right_contour_image = right_smooth_image.clone();
    drawContour(left_contour_image, left_image_contour);
    drawContour(right_contour_image, right_image_contour);
    drawLines(left_contour_image, leftBestTwoLines);
    drawLines(right_contour_image, rightBestTwoLines);

//    ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(left_contour_image.data,left_contour_image.cols,left_contour_image.rows,left_contour_image.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
//    ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(right_contour_image.data,right_contour_image.cols,right_contour_image.rows,right_contour_image.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));

}

//3. Get the normal direction angle and magnitude
void MainWindow::on_Calculate_Button_clicked()
{
     int left_image_extremePoint_index, right_image_extremePoint_index;

     left_image_Gradient = getGradient(left_smooth_image, left_image_contour);
     left_image_result = getAngleMagnitude(left_image_Gradient);
     left_image_extremePoint_index = findExtremePoint(left_image_Gradient);

     right_image_Gradient = getGradient(right_smooth_image, right_image_contour);
     right_image_result = getAngleMagnitude(right_image_Gradient);
     right_image_extremePoint_index = findExtremePoint(right_image_Gradient);

     Point left_image_extremePoint = left_image_contour[left_image_extremePoint_index];
     Point right_image_extremePoint = right_image_contour[right_image_extremePoint_index];

     Mat show_left_image_result = left_smooth_image.clone();
     Mat show_right_image_result  = right_smooth_image.clone();

     drawMarker(show_left_image_result,left_image_extremePoint,Scalar(0,255,0),MARKER_TILTED_CROSS,12,7,8);
     drawMarker(show_right_image_result,right_image_extremePoint,Scalar(0,255,0),MARKER_TILTED_CROSS,12,7,8);

     //Ground Truth (Label Data)
     Point Left_ground, Right_ground;
     Left_ground.x = get<0>(left_image_groundTruth);
     Left_ground.y = get<1>(left_image_groundTruth);
     Right_ground.x = get<0>(right_image_groundTruth) - 200; //because of crop image
     Right_ground.y = get<1>(right_image_groundTruth);

     drawMarker(show_left_image_result,Left_ground,Scalar(0,0,255),MARKER_SQUARE,6,7,8);
     drawMarker(show_right_image_result,Right_ground,Scalar(0,0,255),MARKER_SQUARE,6,7,8);

     //Detection Position
//     ui->Left_x_detect->setText(QString::number(left_image_extremePoint.x));
//     ui->Left_y_detect->setText(QString::number(left_image_extremePoint.y));
//     ui->Right_x_detect->setText(QString::number(right_image_extremePoint.x));
//     ui->Right_y_detect->setText(QString::number(right_image_extremePoint.y));

//     //G.T. Position
//     ui->Left_x_GT->setText(QString::number(Left_ground.x));
//     ui->Left_y_GT->setText(QString::number(Left_ground.y));
//     ui->Right_x_GT->setText(QString::number(Right_ground.x));
//     ui->Right_y_GT->setText(QString::number(Right_ground.y));

//     //Different Detection Position <-> G.T.
//     double x_diff_left = DIFF_ABS(left_image_extremePoint.x, Left_ground.x);
//     double y_diff_left = DIFF_ABS(left_image_extremePoint.y, Left_ground.y);
//     double x_diff_right = DIFF_ABS(right_image_extremePoint.x, Right_ground.x);
//     double y_diff_right = DIFF_ABS(right_image_extremePoint.y, Right_ground.y);

//     ui->diff_x_left->setText(QString::number(x_diff_left));
//     ui->diff_y_left->setText(QString::number(y_diff_left));
//     ui->diff_x_right->setText(QString::number(x_diff_right));
//     ui->diff_y_right->setText(QString::number(y_diff_right));

//     ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(show_left_image_result.data,show_left_image_result.cols,show_left_image_result.rows,show_left_image_result.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
//     ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(show_right_image_result.data,show_right_image_result.cols,show_right_image_result.rows,show_right_image_result.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));

}

//Magnitude, angle data graph oputput
void MainWindow::on_Show_Graph_Button_clicked(){

//    if(ui->radioButton->isChecked() == 1 || (ui->radioButton->isChecked() == 0 && ui->radioButton_2->isChecked() == 0)){
//        set_data(left_image_result, left_image_Gradient);
//    } else{
//        set_data(right_image_result, right_image_Gradient);
//    }

//    plot_graph();
}

//Data Insert fucntion
void MainWindow::set_data(tuple<vector<double>, vector<double>> image_result, vector<tuple<double, double>> image_Gradient)
{
//    qv_x.clear();
//    for(unsigned int i = 0; i < get<0>(image_result).size(); i++){
//        qv_x.append(i);
//    }
//    qv_x2 = qv_x;
//    qv_x3 = qv_x;
//    qv_x4 = qv_x;

//    qv_y4 = QVector<double>::fromStdVector(get<0>(image_result));
//    qv_y3 = QVector<double>::fromStdVector(get<1>(image_result));

//    qv_y.clear();
//    qv_y2.clear();
//    for(unsigned int i = 0; i < image_Gradient.size(); i++){
//        qv_y.append(get<0>(image_Gradient[i]));
//        qv_y2.append(get<1>(image_Gradient[i]));
//    }

}

void MainWindow::plot_graph()
{
    //Just Draw data of add_data function
//    ui->widget->graph(0)->setData(qv_x,qv_y);
//    ui->widget->graph(1)->setData(qv_x2,qv_y2);
//    ui->widget->rescaleAxes();
//    ui->widget->replot();
//    ui->widget->update();

//    ui->widget_2->graph(0)->setData(qv_x3,qv_y3);
//    ui->widget_2->rescaleAxes();
//    ui->widget_2->replot();
//    ui->widget_2->update();

//    ui->widget_3->graph(0)->setData(qv_x4,qv_y4);
//    ui->widget_3->rescaleAxes();
//    ui->widget_3->replot();
//    ui->widget_3->update();

}
