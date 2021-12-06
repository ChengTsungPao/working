#ifndef VIRTUALPOINTDETECTION_H
#define VIRTUALPOINTDETECTION_H




#include <QtCore>
#include "QIODevice"
#include "AppDoc.h"
#include "AlignProcess.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>


using namespace std;
//using namespace cv;

//-----------------------------------------------------------------
//Virtaul Point Detection
class VirtualPointDetection : public QObject
{
    Q_OBJECT

public:
    explicit VirtualPointDetection();
    ~VirtualPointDetection();

public:
    void Testprint();
    bool FindVirtualPoint(cv::Mat input1,cv::Mat input2, cv::Mat* img, cv::Mat* img2, CoorData* cam1_coor, CoorData* cam2_coor);



};

//-----------------------------------------------------------------


#endif // VIRTUALPOINTDETECTION_H
