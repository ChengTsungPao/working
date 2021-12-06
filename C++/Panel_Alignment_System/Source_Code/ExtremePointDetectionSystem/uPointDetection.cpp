#include <uPointDetection.h>

struct myclass_judge_x_coordinate{
    bool operator() (cv::Point pt1, cv::Point pt2) {return (pt1.x < pt2.x);}
}myobject_x;


struct myclass_judge_y_coordinate{
    bool operator() (cv::Point pt1, cv::Point pt2) {return (pt1.y < pt2.y);}
}myobject_y;


