#include "VirtualPointDetection.h"
#include "mainwindow.h"

#include <QtCore>

using namespace std;
//using namespace cv;

VirtualPointDetection::VirtualPointDetection(){

}

VirtualPointDetection::~VirtualPointDetection(){

}

struct myclass_judge_x_coordinate{
    bool operator() (cv::Point pt1, cv::Point pt2) {return (pt1.x < pt2.x);}
}myobject_x_extern;


struct myclass_judge_y_coordinate{
    bool operator() (cv::Point pt1, cv::Point pt2) {return (pt1.y < pt2.y);}
}myobject_y_extern;

bool VirtualPointDetection::FindVirtualPoint(cv::Mat input1, cv::Mat input2, cv::Mat* img, cv::Mat* img2, CoorData* cam1_coor, CoorData* cam2_coor){

    //input variable
    bool result_in=true;
    cv::Mat in1 = input1;
    cv::Mat in2 = input2;

    //Mat for Preprocessing
    cv::Mat gray, gray2;
    cv::Mat result_el, result_el2;

    //Result Coordinates
    CoorData coor_result_1, coor_result_2;
    unsigned int x_c1, y_c1, x_c2, y_c2;

    //1. Convert Image format, noise remove and Threshold
    cv::cvtColor(in1,gray,CV_BGR2GRAY);
    cv::GaussianBlur(gray,gray,Size(5,5),0,0);
    cv::threshold(gray,gray,45,255,THRESH_BINARY);

    cv::cvtColor(in2,gray2,CV_BGR2GRAY);
    cv::GaussianBlur(gray2,gray2,Size(5,5),0,0);
    cv::threshold(gray2,gray2,45,255,THRESH_BINARY);

    //2. Closing Process(Erode -> dilate)
    cv::dilate(gray,result_el,Mat::ones(Size(5,5),CV_8UC1),Point(-1,-1),5); //modify iteration 2->5 2021.06.22
    cv::erode(result_el,result_el,Mat::ones(Size(5,5),CV_8UC1),Point(-1,-1),5);
    cv::dilate(gray2,result_el2,Mat::ones(Size(5,5),CV_8UC1),Point(-1,-1),5); //modify iteration 2->5 2021.06.22
    cv::erode(result_el2,result_el2,Mat::ones(Size(5,5),CV_8UC1),Point(-1,-1),5);

    //3. Find Contour
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    vector<Point> final_con_pt_x;//Point vector for one contour obtained after find contour(x cordinate)
    vector<Point> final_con_pt_y;//Point vector for one contour obtained after find contour(y cordinate)


    vector<vector<Point>> contours2;
    vector<Vec4i> hierarchy2;
    vector<Point> final_con_pt_x2;//Point vector for one contour obtained after find contour(x cordinate)
    vector<Point> final_con_pt_y2;//Point vector for one contour obtained after find contour(y cordinate)

    /********************************************************************************/
    cv::findContours(result_el,contours,hierarchy,RETR_EXTERNAL,CHAIN_APPROX_SIMPLE);
    final_con_pt_x.clear();
    final_con_pt_x.assign(contours[0].begin(), contours[0].end());
    final_con_pt_y.clear();
    final_con_pt_y.assign(contours[0].begin(), contours[0].end());
    /********************************************************************************/
    /********************************************************************************/
    cv::findContours(result_el2,contours2,hierarchy2,RETR_EXTERNAL,CHAIN_APPROX_SIMPLE);
    final_con_pt_x2.clear();
    final_con_pt_x2.assign(contours2[0].begin(), contours2[0].end());
    final_con_pt_y2.clear();
    final_con_pt_y2.assign(contours2[0].begin(), contours2[0].end());
    /********************************************************************************/


    //4. Sorting Contour Points
    std::sort(final_con_pt_x.begin(), final_con_pt_x.end(), myobject_x_extern);
    std::sort(final_con_pt_y.begin(), final_con_pt_y.end(), myobject_y_extern);

    std::sort(final_con_pt_x2.begin(), final_con_pt_x2.end(), myobject_x_extern);
    std::sort(final_con_pt_y2.begin(), final_con_pt_y2.end(), myobject_y_extern);


    int idx=0, largestComp=0;
    double maxArea=0;
    char Val_detect_x[10];
    char Val_detect_y[10];

    int idx2=0, largestComp2=0;
    double maxArea2=0;
    char Val_detect_x2[10];
    char Val_detect_y2[10];


    for( ; idx>=0; idx=hierarchy[idx][0]){
        const vector<Point>& c = contours[idx];
        double area = fabs(contourArea(Mat(c)));
        if(area > maxArea)
        {
            maxArea = area;
            largestComp = idx;
        }
    }

    for( ; idx2>=0; idx2=hierarchy2[idx2][0]){
        const vector<Point>& c2 = contours2[idx2];
        double area2 = fabs(contourArea(Mat(c2)));
        if(area2 > maxArea2)
        {
            maxArea2 = area2;
            largestComp2 = idx2;
        }
    }


    //5. draw the contour and virtual point at Mat
    /***********************************************************************************************/
    cv::drawContours(in1, contours, largestComp, Scalar(255,0,255), 1);
    cv::drawMarker(in1, final_con_pt_x.front(), Scalar(0,0,255),MARKER_TILTED_CROSS,10,2);
    cv::drawMarker(in1, final_con_pt_y.back(), Scalar(0,0,255),MARKER_TILTED_CROSS,10,2);

    cv::line(in1, Point(final_con_pt_x.front().x, 0), Point(final_con_pt_x.front().x, 480),Scalar(0,0,255),3);
    cv::line(in1, Point(0, final_con_pt_y.back().y), Point(640, final_con_pt_y.back().y),Scalar(0,0,255),3);

    cv::drawMarker(in1, Point(final_con_pt_x.front().x, final_con_pt_y.back().y), Scalar(0,255,0),MARKER_CROSS,10,2);


    sprintf_s(Val_detect_x, "X: %d",final_con_pt_x.front().x);
    sprintf_s(Val_detect_y, "Y: %d",final_con_pt_y.back().y);


    x_c1 = final_con_pt_x.front().x;
    y_c1 = final_con_pt_y.back().y;

    coor_result_1.x = x_c1;
    coor_result_1.y = y_c1;

    cv::putText(in1, Val_detect_x, Point(50,410),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);
    cv::putText(in1, Val_detect_y, Point(50,430),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);


    //temporay draw cross mark
    /*
    drawMarker(img, Point(290, 210), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(320, 210), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(350, 210), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(290, 240), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(320, 240), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(350, 240), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(290, 270), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(320, 270), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(350, 270), Scalar(0,255,0),MARKER_CROSS,15,2);
    */

    cv::cvtColor(in1,in1,CV_BGR2RGB); //Opencv Mat -> Qt QImage Data Transform
    /***********************************************************************************************/


    /***********************************************************************************************/
    cv::drawContours(in2, contours2, largestComp2, Scalar(255,0,255), 1);
    cv::drawMarker(in2, final_con_pt_x2.back(), Scalar(0,0,255),MARKER_TILTED_CROSS,10,2);
    cv::drawMarker(in2, final_con_pt_y2.back(), Scalar(0,0,255),MARKER_TILTED_CROSS,10,2);

    cv::line(in2, Point(final_con_pt_x2.back().x, 0), Point(final_con_pt_x2.back().x, 480),Scalar(0,0,255),3);
    cv::line(in2, Point(0, final_con_pt_y2.back().y), Point(640, final_con_pt_y2.back().y),Scalar(0,0,255),3);

    cv::drawMarker(in2, Point(final_con_pt_x2.back().x, final_con_pt_y2.back().y), Scalar(0,255,0),MARKER_CROSS,10,2);


    sprintf_s(Val_detect_x2, "X: %d",final_con_pt_x2.back().x);
    sprintf_s(Val_detect_y2, "Y: %d",final_con_pt_y2.back().y);


    x_c2 = final_con_pt_x2.back().x;
    y_c2 = final_con_pt_y2.back().y;

    coor_result_2.x = x_c2;
    coor_result_2.y = y_c2;

    cv::putText(in2, Val_detect_x2, Point(50,410),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);
    cv::putText(in2, Val_detect_y2, Point(50,430),FONT_HERSHEY_PLAIN,1,Scalar(0,255,0),2);


    //temporay draw cross mark
    /*
    drawMarker(img, Point(290, 210), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(320, 210), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(350, 210), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(290, 240), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(320, 240), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(350, 240), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(290, 270), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(320, 270), Scalar(0,255,0),MARKER_CROSS,15,2);
    drawMarker(img, Point(350, 270), Scalar(0,255,0),MARKER_CROSS,15,2);
    */

    cv::cvtColor(in2,in2,CV_BGR2RGB); //Opencv Mat -> Qt QImage Data Transform
    /***********************************************************************************************/

    //return variable
    *img = in1;
    *img2 = in2;
    *cam1_coor = coor_result_1;
    *cam2_coor = coor_result_2;
    return result_in;
}

void VirtualPointDetection::Testprint(){
    cout << "VirtualPoint" << endl;
}


