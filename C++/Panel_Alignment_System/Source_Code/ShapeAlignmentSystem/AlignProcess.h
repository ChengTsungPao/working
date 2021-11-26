//Align진행 Thread
#ifndef ALIGNPROCESS_H
#define ALIGNPROCESS_H




#include <QtCore>
#include "QIODevice"
#include "math.h"
#include "vector"
#include "cstdlib"
#include "stdint.h"
#include "stdbool.h"
#include "AppDoc.h"
#include "VirtualPointDetection.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>




//----------------------------------------------------------------
//STEP DEFINE (Aftertime need to rename)
#define ALIGN_STEP1     0
#define ALIGN_STEP2     1
#define ALIGN_STEP3     2
#define ALIGN_STEP4     3
#define ALIGN_STEP5     4

#define CALI_STEP1      0
#define CALI_STEP2      1
#define CALI_STEP3      2
#define CALI_STEP4      3

//Align
#define PI          3.14159265358979323846
//#define R           42.43
#define ThetaX1     315
#define ThetaX2     135
#define ThetaY      225
#define MM2PULSE    1600

//Calibration
#define PPR 1600


using namespace std;
//using namespace cv;



//-----------------------------------------------------------------
//Align Sequence
class AlignProcess : public QObject
{
    Q_OBJECT

public:
    explicit AlignProcess();
    ~AlignProcess();

public:
    bool bStatusAlignPro;

public slots:
    void process(); //여기서 프로세스 내용 진행

public:
    // Get, Set Function
    void SetDistanceCal(double val) { dis_cal = val; }
    double GetDistanceCal() { return dis_cal; }
    void SetAngCal(double val) { ang_cal = val; }
    float GetAngCal() { return ang_cal; }
    void SetTOL(double tol) { Tol = tol; }
    double GetTOL() { return Tol; }
    void SetPosCal(std::vector<CoorData>);
    void SetPosRef(std::vector<CoorData>);
    void ShiftVc(double x, double y);
    int* GetPulResult() { return pulse_final; }
    double GetFinalAng() { return ang_final; }
    CoorData GetPlatCenter() { return pc; }
    CoorData GetPlatCenter2() { return pc2; }
    double GetPcRadius() { return radius_cal1; }
    double GetPcRadius2() { return radius_cal2; }
    double GetPixResolution() { return l; }
    CoorData GetOrigin2() { return origin_cam2; }
    CoorData GetDiffPos() { return pos_diff; }


    // Calibration
    void SolvePul2Pix();
    void RunCalibration();

    // Alignment
    void RunAlignment(std::vector<CoorData>);
    bool isRsltOK(std::vector<CoorData> una_pos, double &diff1, double &diff2);

    // Tool
    void Ang2Pulse(int* , double, double);
    void Pulse2MM(double* dst, int* pul);
    void Clear();





private:
    int nStep;
    double l;                         // How many pulses for 1 pixel
    double dis_cal;                   // calibration distance
    double ang_cal;                   // calibration angle
    double radius_cal1;               // radius of pc to cal points
    double radius_cal2;               // radius of pc to cal points for cam2

    double theta_bias;                // Bias angle
    int* pulse_final;                 // Final pulse results
    double ang_final;                 // Final rotate to parallel angle
    double Tol;                       // Testing tolerance
    double delta_1;
    double delta_2;



    std::vector<CoorData> una_pos;
    std::vector<CoorData> una_pos_2;

    std::vector<CoorData> pos_cal1; // calibration positions for solve "l", FOV 1
    std::vector<CoorData> pos_cal2; // calibration positions for solve "l", FOV 2
    CoorData *pos_4pc1;             // position for solve the Pc, FOV 1
    CoorData *pos_4pc2;             // position for solve the Pc, FOV 2

    CoorData pc;                      //platform rotation center1
    CoorData pc2;                     //platform rotation center2
    CoorData origin_cam2;             //The origin coordinate of cam2
    std::vector<CoorData> detect_pos; //cam detect(Cam1, Cam2) coordinate data
    CoorData pos_diff;                //Position btw ref and unalingment pt differnet
    CoorData pos_ref1;                //Position for reference, FOV1
    CoorData pos_ref2;                //Position for reference, FOV2

    //---------------------------Sequence Function-------------------------//
    void AlignStartReqChk(void);
    void AlignStart(void);
    void Align_mainprocess(void);
    void Align_judge(void);
    void Align_finish(void);


    //---------------------------Alignment Algorithm Function--------------//
    CoorData GetDirVec(LinePara LP, int dir);
    double GetDistanceOm(CoorData pl, CoorData p2, double theta);
    CoorData SolvePlatformCenter(CoorData p1, CoorData p2, double theta, int dir);
    LinePara GetLinePara(CoorData p1, CoorData p2);
    CoorData SolveRightOriginPt(CoorData p1, CoorData p2);
    double SolveBiasAng(CoorData);
    double Solve2LineAng(CoorData p1, CoorData p2, CoorData p3, CoorData p4);
    CoorData FindEstPos(CoorData, CoorData, double);

    //---------------------------Tool Function----------------------------//
    double _Deg2rad(double deg) { return deg * PI / 180.0; } //Deg<->Radian 변환. 사람들은 deg선호하지만 컴퓨터는 주로 Radian으로 계산.
    double _Rad2deg(double rad) { return rad * 180.0 / PI; }
    CoorData _AddCoor(CoorData, CoorData);
    CoorData _SubCoor(CoorData, CoorData);
    double  _LenOfCoor(CoorData c) {return sqrt(pow(c.x, 2.0) + pow(c.y, 2.0));}

signals:
    void finished();
    void error(QString err);

};

#endif // ALIGNPROCESS_H
