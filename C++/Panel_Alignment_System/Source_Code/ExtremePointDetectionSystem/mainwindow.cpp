#include "mainwindow.h"

#define DIFF_ABS(X,Y) ((X)>(Y)? (X)-(Y) : (Y)-(X))


using namespace std;
//using namespace cv;

MainWindow* ui_ext = NULL;


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);



    ui_ext = this;
    bThreadStatus = false;
    bchoose_graph = false;
    //#1 graph screen
    //graph1 gx blue
    ui->widget->addGraph();
    ui->widget->graph(0)->setLineStyle(QCPGraph::lsLine);
    ui->widget->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
    //graph2 gy Red
    ui->widget->addGraph();
    ui->widget->graph(1)->setLineStyle(QCPGraph::lsLine);
    ui->widget->graph(1)->setPen(QPen(QColor(255, 0, 0), 2));

    ui->widget->xAxis->setLabel("Boundary Point Index");
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
    ui->widget_2->xAxis->setLabel("Boundary Point Index");
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
    ui->widget_3->xAxis->setLabel("Boundary Point Index");
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


//    connect(ui->radioButton, SIGNAL(clicked()), this, SLOT(radio_button_left()));
//    connect(ui->radioButton_2, SIGNAL(clicked()), this, SLOT(radio_button_right()));






}

MainWindow::~MainWindow()
{
    delete ui;
}


bool compare(const tuple<int, int, float>& a, const tuple<int, int, float>& b){
    return (get<2>(a) > get<2>(b));
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








void MainWindow::showPopup() //show the pop-up
{


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

    ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(show_left_image.data, show_left_image.cols, show_left_image.rows, show_left_image.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
    ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(show_right_image.data, show_right_image.cols, show_right_image.rows, show_right_image.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));
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

    ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(left_contour_image.data,left_contour_image.cols,left_contour_image.rows,left_contour_image.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
    ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(right_contour_image.data,right_contour_image.cols,right_contour_image.rows,right_contour_image.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));

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
     ui->Left_x_detect->setText(QString::number(left_image_extremePoint.x));
     ui->Left_y_detect->setText(QString::number(left_image_extremePoint.y));
     ui->Right_x_detect->setText(QString::number(right_image_extremePoint.x));
     ui->Right_y_detect->setText(QString::number(right_image_extremePoint.y));

     //G.T. Position
     ui->Left_x_GT->setText(QString::number(Left_ground.x));
     ui->Left_y_GT->setText(QString::number(Left_ground.y));
     ui->Right_x_GT->setText(QString::number(Right_ground.x));
     ui->Right_y_GT->setText(QString::number(Right_ground.y));

     //Different Detection Position <-> G.T.
     double x_diff_left = DIFF_ABS(left_image_extremePoint.x, Left_ground.x);
     double y_diff_left = DIFF_ABS(left_image_extremePoint.y, Left_ground.y);
     double x_diff_right = DIFF_ABS(right_image_extremePoint.x, Right_ground.x);
     double y_diff_right = DIFF_ABS(right_image_extremePoint.y, Right_ground.y);

     ui->diff_x_left->setText(QString::number(x_diff_left));
     ui->diff_y_left->setText(QString::number(y_diff_left));
     ui->diff_x_right->setText(QString::number(x_diff_right));
     ui->diff_y_right->setText(QString::number(y_diff_right));

     ui->lbl_img1->setPixmap(QPixmap::fromImage(QImage(show_left_image_result.data,show_left_image_result.cols,show_left_image_result.rows,show_left_image_result.step,QImage::Format_RGB888).scaled(ui->lbl_img1->width(),ui->lbl_img1->height(),Qt::KeepAspectRatio)));
     ui->lbl_img2->setPixmap(QPixmap::fromImage(QImage(show_right_image_result.data,show_right_image_result.cols,show_right_image_result.rows,show_right_image_result.step,QImage::Format_RGB888).scaled(ui->lbl_img2->width(),ui->lbl_img2->height(),Qt::KeepAspectRatio)));

}

//Magnitude, angle data graph oputput
void MainWindow::on_Show_Graph_Button_clicked(){

    if(ui->radioButton->isChecked() || (ui->radioButton->isChecked() == 0 && ui->radioButton_2->isChecked() == 0)){
        set_data(left_image_result, left_image_Gradient);
    } else{
        set_data(right_image_result, right_image_Gradient);
    }

    plot_graph();
}

//Data Insert fucntion
void MainWindow::set_data(tuple<vector<double>, vector<double>> image_result, vector<tuple<double, double>> image_Gradient)
{
    qv_x.clear();
    for(unsigned int i = 0; i < get<0>(image_result).size(); i++){
        qv_x.append(i);
    }
    qv_x2 = qv_x;
    qv_x3 = qv_x;
    qv_x4 = qv_x;

    qv_y4 = QVector<double>::fromStdVector(get<0>(image_result));
    qv_y3 = QVector<double>::fromStdVector(get<1>(image_result));

    qv_y.clear();
    qv_y2.clear();
    for(unsigned int i = 0; i < image_Gradient.size(); i++){
        qv_y.append(get<0>(image_Gradient[i]));
        qv_y2.append(get<1>(image_Gradient[i]));
    }

}

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
