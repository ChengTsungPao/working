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

    return result_in;
}

void VirtualPointDetection::Testprint(){
    cout << "VirtualPoint" << endl;
}


