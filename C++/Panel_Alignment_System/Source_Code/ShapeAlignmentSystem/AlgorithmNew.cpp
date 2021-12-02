#include <QFileDialog>
#include <QJsonObject>
#include <QJsonDocument>
#include <QJsonArray>
#include <QFile>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <vector>
#include <tuple>
#include <Canny_Ben.h>
//#include <opencv2/core/mat.hpp>

using namespace std;
using namespace cv;

Mat Image_Load(QString left_image_filename ,QString right_image_filename);
vector<Point> findBestContour(vector<vector<Point>> contours);
vector<Point> orderContour(vector<Point> contour, int x, int y);
void Find_Contour_Button(Mat left_image, Mat right_image);


Mat Image_Load(QString left_image_filename ,QString right_image_filename){

        Mat g_InImg1 = cv::imread(left_image_filename.toStdString());
        Mat g_InImg2 = cv::imread(right_image_filename.toStdString());

}

vector<Point> findBestContour(vector<vector<Point>> contours){
    vector<Point> ans = contours[0];

    for(int i = 1; i < contours.size(); i++){
        if(contours[i].size() > ans.size()){
            ans = contours[i];
        }
    }
    return ans;
}


vector<Point> orderContour(vector<Point> contour, int x, int y){
    int x_, y_;
    float angle;
    vector<tuple<float, Point>> data;
//    for(int i = 0; i < contour.size(); i++){
//        x_ = contour[i].x;
//        y_ = contour[i].y;
//        angle = (float)(y - y_) / (x - x_);
//        data.push_back(make_tuple(angle, Point(x, y)));
//    }
//    sort(data.begin(), data.end());

    vector<Point> ans;
    for(int i = 0; i < data.size(); i++){
        ans.push_back(get<1>(data[i]));
    }

    return ans;
}


void Find_Contour_Button(Mat left_image, Mat right_image)
{

    //Data Initialize
    if(!left_image.empty()){ left_image.zeros(left_image.rows, left_image.cols, CV_8UC3);}
    if(!right_image.empty()){ right_image.zeros(right_image.rows, right_image.cols, CV_8UC3);}


    //ROI Setting
    left_image = left_image(cv::Rect(0,0,1080,660)); //Left
    right_image = right_image(cv::Rect(200,0,1080,660)); //Right


    //Remove noise
    //Left
    Mat left_image_smooth;
    cv::medianBlur(left_image,left_image_smooth,11);
    cv::GaussianBlur(left_image_smooth,left_image_smooth,Size(5,5),0,0);


    //Right
    Mat right_image_smooth;
    cv::medianBlur(right_image,right_image_smooth,11);
    cv::GaussianBlur(right_image_smooth,right_image_smooth,Size(5,5),0,0);


    //shape match mat
    Mat left_image_shape, right_image_shape;
    left_image_shape = left_image_smooth.clone();
    right_image_shape = right_image_smooth.clone();
    cv::cvtColor(left_image_shape, left_image_shape, CV_BGR2GRAY);
    cv::cvtColor(right_image_shape, right_image_shape, CV_BGR2GRAY);

//    cv::imshow("left_image_shape",left_image_shape);
//    cv::imshow("right_image_shape",right_image_shape);


    Mat Edge_Left, Edge_Right;
    Mat LX, LY, RX, RY;
    Canny_Ben(left_image_shape,Edge_Left,70,130,3,0,LX,LY); //Get Edge
    Canny_Ben(right_image_shape,Edge_Right,70,130,3,0,RX,RY); //Get Edge
    cv::imshow("Left",Edge_Left);
    cv::imshow("Right",Edge_Right);


    //Left
    Mat left_image_canny;
    Mat left_image_SobelX, left_image_SobelY;
    Canny_Ben(left_image_smooth,left_image_canny,70,130,3,0,left_image_SobelX,left_image_SobelY); //get the Gx, Gy
    left_image_SobelX.convertTo(left_image_SobelX,CV_64F);
    left_image_SobelY.convertTo(left_image_SobelY,CV_64F);

    //Right
    Mat right_image_canny;
    Mat right_image_SobelX, right_image_SobelY;
    Canny_Ben(right_image_smooth,right_image_canny,70,130,3,0,right_image_SobelX,right_image_SobelY); //get the Gx, Gy
    right_image_SobelX.convertTo(right_image_SobelX,CV_64F);
    right_image_SobelY.convertTo(right_image_SobelY,CV_64F);

    vector<vector<Point>> left_image_contours;
    cv::findContours(Edge_Left, left_image_contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);
    vector<vector<Point>> right_image_contours;
    cv::findContours(Edge_Right, right_image_contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);

    vector<Point> left_image_contour = findBestContour(left_image_contours);
    vector<Point> right_image_contour = findBestContour(right_image_contours);

    left_image_contour = orderContour(left_image_contour, 0, 0);
    right_image_contour = orderContour(right_image_contour, 1080, 0);


}


