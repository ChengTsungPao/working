#include "mainwindow.h"

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




void MainWindow::showPopup() //show the pop-up
{


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

    // test in current
    g_InImg1 = left_image.clone();
    g_InImg2 = right_image.clone();

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

    if(bchoose_graph){
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
