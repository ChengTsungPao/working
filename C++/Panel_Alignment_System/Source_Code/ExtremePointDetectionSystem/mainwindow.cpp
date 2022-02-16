#include "mainwindow.h"

#define DIFF_ABS(X,Y) ((X)>(Y)? (X)-(Y) : (Y)-(X))

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////// UI setup //////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);


    // Angle plot

    ui->widget_angle->addGraph();
    ui->widget_angle->graph(0)->setLineStyle(QCPGraph::lsLine);
    ui->widget_angle->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
    ui->widget_angle->xAxis->setLabel("Boundary Point Index");
    // axis
    ui->widget_angle->yAxis->setLabel("Angle");
    ui->widget_angle->xAxis->rescale(false);
    ui->widget_angle->yAxis->rescale(false);


    // Gradient plot

    // Gx
    ui->widget_gradient->addGraph();
    ui->widget_gradient->graph(0)->setLineStyle(QCPGraph::lsLine);
    ui->widget_gradient->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
    // Gy
    ui->widget_gradient->addGraph();
    ui->widget_gradient->graph(1)->setLineStyle(QCPGraph::lsLine);
    ui->widget_gradient->graph(1)->setPen(QPen(QColor(255, 0, 0), 2));
    // axis
    ui->widget_gradient->xAxis->setLabel("Boundary Point Index");
    ui->widget_gradient->yAxis->setLabel("Gx,Gy");
    ui->widget_gradient->xAxis->rescale(false);
    ui->widget_gradient->yAxis->rescale(false);


    // Magnitude plot

    ui->widget_magnitude->addGraph();
    ui->widget_magnitude->graph(0)->setLineStyle(QCPGraph::lsLine);
    ui->widget_magnitude->graph(0)->setPen(QPen(QColor(0, 0, 255), 2));
    ui->widget_magnitude->xAxis->setLabel("Boundary Point Index");
    // axis
    ui->widget_magnitude->yAxis->setLabel("Magnitude");
    ui->widget_magnitude->xAxis->rescale(false);
    ui->widget_magnitude->yAxis->rescale(false);

}

MainWindow::~MainWindow()
{
    delete ui;
}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////// Tsung-Pao Cheng //////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

    left_image_groundTruth = readJsonFile(left_image_path.split(".png").at(0) + ".json");
    right_image_groundTruth = readJsonFile(right_image_path.split(".png").at(0) + ".json");

    Image_Load(left_image_path.toStdString(), left_image);
    Image_Load(right_image_path.toStdString(), right_image);
//    getExtremePoint(left_image_path.toStdString(), 'L', true);

//    left_image_groundTruth = rotatedImage(left_image, left_image_groundTruth, -30);
//    right_image_groundTruth = rotatedImage(right_image, right_image_groundTruth, -30);

    Mat show_left_image = left_image.clone();
    Mat show_right_image = right_image.clone();

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
     // left_image_extremePoint_index = findExtremePointByGradient(left_image_Gradient);
     left_image_extremePoint_index = findExtremePointByMinMax(left_image_result);

     right_image_Gradient = getGradient(right_smooth_image, right_image_contour);
     right_image_result = getAngleMagnitude(right_image_Gradient);
     // right_image_extremePoint_index = findExtremePointByGradient(right_image_Gradient);
     right_image_extremePoint_index = findExtremePointByMinMax(right_image_result);

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
     Right_ground.x = get<0>(right_image_groundTruth) - 200 * ROISWITCH; //because of crop image
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
        plot_graph(left_image_result, left_image_Gradient);
    } else{
        plot_graph(right_image_result, right_image_Gradient);
    }

}

void MainWindow::plot_graph(tuple<vector<double>, vector<double>> image_result, vector<tuple<double, double>> image_Gradient)
{

    QVector<double> index_of_boundary;
    for(unsigned int i = 0; i < get<0>(image_result).size(); i++){
        index_of_boundary.append(i);
    }

    QVector<double> Gx, Gy;
    for(unsigned int i = 0; i < image_Gradient.size(); i++){
        Gx.append(abs(get<0>(image_Gradient[i])));
        Gy.append(abs(get<1>(image_Gradient[i])));
    }
    ui->widget_gradient->graph(0)->setData(index_of_boundary, Gx);
    ui->widget_gradient->graph(1)->setData(index_of_boundary, Gy);
    ui->widget_gradient->rescaleAxes();
    ui->widget_gradient->replot();
    ui->widget_gradient->update();

    QVector<double> angle = QVector<double>::fromStdVector(get<1>(image_result));
    ui->widget_angle->graph(0)->setData(index_of_boundary, angle);
    ui->widget_angle->rescaleAxes();
    ui->widget_angle->replot();
    ui->widget_angle->update();

    QVector<double> magnitude = QVector<double>::fromStdVector(get<0>(image_result));
    ui->widget_magnitude->graph(0)->setData(index_of_boundary, magnitude);
    ui->widget_magnitude->rescaleAxes();
    ui->widget_magnitude->replot();
    ui->widget_magnitude->update();

}
