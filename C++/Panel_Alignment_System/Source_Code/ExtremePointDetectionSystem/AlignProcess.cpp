#include "AlignProcess.h"
#include "mainwindow.h"

#include <QtCore>




VirtualPointDetection* cornerdetector = new VirtualPointDetection();


AlignProcess::AlignProcess(){
    //생성자에서 heap 영역에(new operator) 데이터 생성 금지!!.
    //왜냐하면, 이 할당은 새로만든 Thread Object가 아닌 MainThread에서 수행되기 때문이다.
    //아래의 Process에서 heap영역 데이터 생성 및 할당.
}

AlignProcess::~AlignProcess(){

}


//1. Align 시작요청 확인(PLC와의 Align Start I/F 안함. Main화면 Start버튼을 Align Start Signal로 처리)
void AlignProcess::AlignStartReqChk(){
    if(bAlignStartReq){
        //Log로 Align 시작 요청확인됬다고 출력
        bAlignStartReq=false;
    }else{
        return;
    }

}

//2. Align 시작. 모터 이동 가능, 모터 이동 중 체크. **추후 확인필요**
void AlignProcess::AlignStart(void){
    if(bMoving || bMovingReq){
        //Log로 모터이동중 or 모터이동요청했다고 출력
        return;
    }
}


//3. AlignmentMainProcess
void AlignProcess::Align_mainprocess(void){

    una_pos.clear();   //Before Alignment(Motor Move) Data
    una_pos_2.clear(); //After  Alignment(Motor Move) Data
    CoorData detect_val;
    double pulse[3] = {0,0,0};
    int *final_pulse;

    // if(!bStatusAlignPro)
    // {
    //     ui_ext->ControlPLC(ui_ext->com, "Zero", nullptr);
    // }

    cv::Mat input_1,input_2;
    cv::Mat out1,out2;
    bool result;
    CoorData cam1_coor, cam2_coor;

    //Measure point by using Algorithm
    result = cornerdetector->FindVirtualPoint(input_1,input_2,&out1,&out2, &cam1_coor, &cam2_coor);


    //Conversion data of coordinates
    //Cam1
    detect_val.x = (double)cam1_coor.x;
    detect_val.y = -1; //The row counts of camera frames - detect pos
    una_pos.push_back(detect_val);
    //Cam2
    detect_val.x = (double)cam2_coor.x;
    detect_val.y = -1; //The row counts of camera frames - detect pos
    una_pos.push_back(detect_val);


    //Process Alignment
    RunAlignment(una_pos);
    final_pulse = GetPulResult();

    //PC -> PLC Data Write
    pulse[0] = GetFinalAng();
    // ui_ext->ControlPLC(ui_ext->com, "Deg", pulse);
    // ui_ext->SetPulse(pulse, final_pulse[0], final_pulse[1], final_pulse[2]);
    // ui_ext->ControlPLC(ui_ext->com, "Rel", pulse);



}

void AlignProcess::Align_judge(void)
{

    //Motor Moving and PLC Communication complete check
    //If didn't Complete return

    cv::Mat input_1,input_2;
    cv::Mat out1,out2;
    bool result;
    CoorData cam1_coor, cam2_coor;
    CoorData detect_val;

    //Measure point by using Algorithm
    result = cornerdetector->FindVirtualPoint(input_1,input_2,&out1,&out2, &cam1_coor, &cam2_coor);


    //Conversion data of coordinates
    //Cam1
    detect_val.x = (double)cam1_coor.x;
    detect_val.y = -1; //The row counts of camera frames - detect pos
    una_pos_2.push_back(detect_val);
    //Cam2
    detect_val.x = (double)cam2_coor.x;
    detect_val.y = -1; //The row counts of camera frames - detect pos
    una_pos_2.push_back(detect_val);


    if(isRsltOK(una_pos_2, delta_1, delta_2))
    {
        //Align complete. Go Next Step(Align Result Data Get, Print Log)
        bAlignComplete = true;
        SetAlignStep(ALIGN_STEP4);

    }
    else
    {
       //Align NG. Retry Align
       double shift_x = GetDiffPos().x;
       double shift_y = GetDiffPos().y;
       //ShiftVc(shift_x,shift_y);
       //nAligncount++;
       SetAlignStep(ALIGN_STEP2);
    }

}


void AlignProcess::Align_finish(void)
{
    //Align finish. Log save, UI Data set and send to Main UI.

    //variable Initialize
    nAlignStep = ALIGN_STEP1;
    //nAligncount = 0;
    bStatusAlignPro = false;
}





void AlignProcess::process(){

        cout << "Align Process Start" << endl;

        //Aling Parameter Initialize ???
//        dis_cal = 0.5;
//        ang_cal = 1.0;
//        Tol = 0.02;

        //STEP, variable  Initialization
        nAlignStep = ALIGN_STEP1;
        bAlignComplete = false;
        //nAligncount = 0;

        while(1)
        {
            QThread::sleep(20);

            if(bStatusAlignPro)
            {
                emit finished();  //finished() => signal
                break;
            }

            // STEP1
            if(nAlignStep == ALIGN_STEP1)
            {
                cout << "START ALIGN CYCLE"<< endl;
                cout << "ALIGN_STEP: %d"<< nAlignStep << endl;
                AlignStartReqChk();
                SetAlignStep(ALIGN_STEP2);

            }


            // STEP2
            if(nAlignStep == ALIGN_STEP2)
            {
                cout << "ALIGN_STEP: %d"<< nAlignStep << endl;
                Align_mainprocess();
                SetAlignStep(ALIGN_STEP3);

            }


            // STEP3
            if(nAlignStep == ALIGN_STEP3)
            {
                cout << "ALIGN_STEP: %d"<< nAlignStep << endl;
                Align_judge();
            }

            // STEP4(Align finish step)
            if(nAlignStep == ALIGN_STEP4)
            {
                cout << "ALIGN_STEP: %d"<< nAlignStep << endl;
                Align_finish();
                break;
            }

            qDebug("AlignProcess");
            cout << "AlignProcess" << endl;

        }
        cout << "Align Process End" << endl;

}



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//--------------------Calibration-----------------------------------------------------------------------------------------------
//------------------------------------------------------------------------------------------------------------------------------
void AlignProcess::RunCalibration()
{
    //Find PC(Platform Center)
    pc  = SolvePlatformCenter(pos_4pc1[0], pos_4pc2[0], ang_cal, 0);
    pc2 = SolvePlatformCenter(pos_4pc1[1], pos_4pc2[1], ang_cal, 1);
    radius_cal1 = _LenOfCoor(_SubCoor(pc, pos_4pc1[0]));
    radius_cal2 = _LenOfCoor(_SubCoor(pc2, pos_4pc1[0]));
    origin_cam2 = SolveRightOriginPt(pc, pc2);

    theta_bias = SolveBiasAng(origin_cam2);
}
//------------------------------------------------------------------------------------------------------------------------------
void AlignProcess::SolvePul2Pix()
{
    //Solve the "l" (l is realation with pixel and pulse. 1pixel당 몇 Pulse?)
    double dl = 0.0;
    double dr = 0.0;
    double ll = 0.0;
    double lr = 0.0;

    //Calibration 시 움직인 좌표들의 길이 합산 (LenOfCoor : 점<->점 거리 계산)
    for(int i=0; i<pos_cal1.size()-1; i++){
        dl += _LenOfCoor(_SubCoor(pos_cal1[i], pos_cal1[i+1]));
    }
    for(int i=0; i<pos_cal2.size()-1; i++){
        dr += _LenOfCoor(_SubCoor(pos_cal2[i], pos_cal2[i+1]));
    }

    //l = cal이동 거리(0.5mm(800pulse, Contrel provided) / {(dl, dr / 이동횟수(=pos_cal1.size()-1)}, 점이 3개면 2번이동))
    //0.5mm = 800pulse
    ll = dis_cal / (dl /(pos_cal1.size()-1));
    lr = dis_cal / (dr /(pos_cal2.size()-1));

    l = (ll + lr) / 2;

}
//------------------------------------------------------------------------------------------------------------------------------
coordata AlignProcess::SolvePlatformCenter(CoorData p1, CoorData p2, double theta, int dir)
{
    //Solve Platform Center(회전중심 구하기. Cam1과 Cam2의 회전중심값 Point(x,y)형태로 구한다. C1=C2이다. 결과값이 다른것은 Cam1->C1, Cam2->C2가 다르기 때문이다.즉 보는관점이 다르기 때문이다.
    CoorData vec_n;
    CoorData point_m;
    CoorData point_O;
    double dis_Om = 0.0;

    //middle point(m)
    point_m.x = (p2.x + p1.x) / 2;
    point_m.y = (p2.y + p1.y) / 2;

    vec_n = GetDirVec(GetLinePara(p1,p2), dir);
    dis_Om = GetDistanceOm(p1, p2, theta);

    point_O.x = point_m.x + vec_n.x * dis_Om;
    point_O.y = point_m.y + vec_n.y * dis_Om;

    return point_O;

}
//------------------------------------------------------------------------------------------------------------------------------
LinePara AlignProcess::GetLinePara(CoorData p1, CoorData p2)
{
    //Calibration 시 선형방정식 산출(ax + by + c인데, c는 무시하고 y = ax + b로 생각)
    //여기서 a와 b의 값을 구한다.

    double m = 0;
    LinePara LP;

    m = p2.x - p1.x; //x 좌표계에서의 p1과 p2의 중심점

    if(m = 0){ //예외상황처리
        LP.a = 10000.0; //기울기 값 +10000으로 임시값
        LP.b = p1.y - LP.a * p1.x;
    }else{
        LP.a = (p2.y - p1.y) / (p2.x - p1.x);
        LP.b = p1.y - LP.a * p1.x;
    }

    return LP;
}
//------------------------------------------------------------------------------------------------------------------------------
CoorData AlignProcess::GetDirVec(LinePara LP, int dir)
{
    //Vector n 을 구한다.

    double yPara = 1.0; //초기값 : LP.a의 값에 따라 값이 변함. 때문에 초기값으로 계산을 쉽게하기 위해 y = ax + b로. 계산 용이성.
    double xPara = LP.a;
    double deno = 1.0;
    CoorData result;

    if(xPara > 0){ //기울기가 +인 경우, yParam(점의 Y좌표)은 +1.0 -> -1.0, 따라서 -y = ax + b
        yPara = -yPara;
    }else{         //기울기가 -인 경우 y=ax+b에서 a값이 -가 됨, 따라서 y = -ax + b
        xPara = -xPara;
    }

    deno = sqrt(xPara*xPara + yPara*yPara); //vector n의 분모. x좌표제곱 + y좌표제곱의 루트
    // 직선방정식을 GetLinePara에서 y = ax + b에서

    //왜 이렇게 되는지 물어봐야 함????
    if(dir){ //right cam (y좌표 1인 직선을 시작기준점 (prot)으로 잡고, right cma은 prot -> prot'으로 이동 시
        result.x = -xPara / deno;
        result.y = -yPara / deno;
    }else{   //left cam
        result.x = xPara / deno;
        result.y = yPara / deno;
    }

    return result;
}
//------------------------------------------------------------------------------------------------------------------------------
double AlignProcess::GetDistanceOm(CoorData p1, CoorData p2, double theta)
{
    //O(회전중심)과 m의 거리 측정
    double dis_Om;
    CoorData point_m;
    double dis_p2m = 0.0;
    point_m.x = (p2.x + p1.x) / 2;
    point_m.x = (p2.x + p1.x) / 2;

    dis_p2m = sqrt(pow(p2.x-point_m.x, 2) + pow(p2.y-point_m.y, 2));
    dis_Om  = dis_p2m * (1 / tan(_Deg2rad(theta)));

    return dis_Om;
}
//------------------------------------------------------------------------------------------------------------------------------
CoorData AlignProcess::SolveRightOriginPt(CoorData p1, CoorData pr)
{
    //1번 CAM기준(1번 CAM영역)으로 2번 CAM의 (0,0)를 계산
    CoorData result;

    result.x = p1.x - pr.x;
    result.y = p1.y - pr.y;

    return result;
}
//------------------------------------------------------------------------------------------------------------------------------
CoorData AlignProcess::_AddCoor(CoorData c1, CoorData c2)
{
    CoorData result;
    result.x = c1.x + c2.x;
    result.y = c1.y + c2.y;

    return result;
}
//------------------------------------------------------------------------------------------------------------------------------
CoorData AlignProcess::_SubCoor(CoorData c1, CoorData c2)
{
    CoorData result;
    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;

    return result;
}
//------------------------------------------------------------------------------------------------------------------------------
double AlignProcess::SolveBiasAng(CoorData rFov){
    return _Rad2deg(atan(rFov.y/rFov.x));
}
//------------------------------------------------------------------------------------------------------------------------------
double AlignProcess::Solve2LineAng(CoorData p1, CoorData p2, CoorData p3, CoorData p4){
    //점 p1, p2 (Reference Point)의 Vector, 점 q1, q2 (detected point)의 Vector구하기
    double len1 = sqrt(pow(p2.x-p1.x, 2) + pow(p2.y-p1.y, 2)); //삼각형의 (빗변)^2 = (밑변)^2 + (높이)^2에서 길이공식 도출.
    double len2 = sqrt(pow(p4.x-p3.x, 2) + pow(p4.x-p3.x, 2));
    //Vector Point 내적 (p1, p2) : p2.x * p1.x + p2.y * p1.y
    //아래는 Vector Line선분이기 때문에 (p2.x - p1.x) * (p4.x - p3.x)
    // A x B = |A||B|cos(theta)에 의해 아래의 식 산출.  |A| = len1, |B| = len2
    double cosValue = ((p2.x - p1.x) * (p4.x - p3.x) + (p2.y - p1.y) * (p4.y - p3.y)) / (len1 * len2);
    double result = _Rad2deg(acos(cosValue));


    //p1-p2 Vector Line기준 위로 p3-p4 Vector Line 위치했을 때는 위에서 계산한 값 그대로
    if((p1.y - p2.y) < (p3.y - p4.y))
        return result;
    //p1-p2 Vector Line기준 아래로 p3-p4 Vector Line 위치했을 때는 위에서 계산한 값에 역수처리.
    //왜냐하면, 위의 계산에서 초기 Vector를 만들때 시작점 p1, q1  종료점 p2, q2로 벡터를 만들었기 떄문이다.
    else
        return -result;

}
//------------------------------------------------------------------------------------------------------------------------------
CoorData AlignProcess::FindEstPos(CoorData Po, CoorData Pc, double theta)
{
    //Solve2LineAng()에서 구한 Theta와 Platform CenterPoint로 EstPoint를 구할 수 있다.
    double theta_in = _Deg2rad(theta); //c++에서 연산하기 위해 degree에서 Radian으로 변환
    CoorData result;

    double m_P1[3][1] = {{Po.x-Pc.x},{Po.y-Pc.y},{1}}; //시작위치(Reference Point). Affine Transform의 시작위치
    double m_R[3][3] = {{cos(theta_in), -sin(theta_in), 0}, {sin(theta_in), cos(theta_in), 0}, {0, 0, 1}}; //Rotation Matrix
    double m_P2[3][1] = {{0},{0},{1}}; //P1과 R의 곱셈연산의 결과 저장배열(Homogenious 좌표계에서는 마지막원소 1이 점을 표현)

    //R x Reference Point = m_P2
    for(int i=0; i<3; i++)
    {
        for(int j=0; j<3; j++)
        {
            m_P2[i][0] += m_R[i][j] * m_P1[j][0];
        }
    }

    //m_P2 + Translation(Platform Center). m_P1에서 Po - Pc하여 연산 후, 다시 +Pc를 하여 다시 기준점을 (0,0)로.
   result.x = m_P2[0][0] + Pc.x;
   result.y = m_P2[1][0] + Pc.y;

   return result;

}
//------------------------------------------------------------------------------------------------------------------------------
void AlignProcess::SetPosCal(std::vector<CoorData> pos)
{
    //Calibratio 위치 Set
    pos_4pc1 = new CoorData[2];
    pos_4pc2 = new CoorData[2];

    if(!pos.empty())
    {
        //Set Calibration 위치 for "l"
        for(int i=0; i<pos.size()-5; i+=2)
        {
            pos_cal1.push_back(pos[i]);   //CAM1 Position : 1,3,5,7
            pos_cal2.push_back(pos[i+1]); //CAM2 Position : 2,4,6,8
        }

        //Set Calibration 위치 for "PlatformCeneter"
        pos_4pc1[0] = pos[pos.size()-4]; //Origin
        pos_4pc1[1] = pos[pos.size()-3]; //1deg

        pos_4pc2[0] = pos[pos.size()-2]; //-1deg
        pos_4pc1[1] = pos.back();        //Origin


    }
}
//------------------------------------------------------------------------------------------------------------------------------
void AlignProcess::SetPosRef(std::vector<CoorData> pos)
{
    //Reference 위치 Set

    if(!pos.empty() && pos.size()>1)
    {
        pos_ref1 = pos[0];
        pos_ref2 = pos[1];
    }
}


void AlignProcess::RunAlignment(std::vector<CoorData> una_pos)
{
    //Alignment Process
    CoorData pos_una1, pos_una2; //Unalignment pos data
    CoorData pos_est;
    CoorData pos_ref2_new;
    double dTheta = 0.0;
    pulse_final = new int [3];


    pos_una1 = una_pos[0]; //1번 Cam측정데이터
    pos_una2 = una_pos[1]; //2번 Cam측정데이터


    //origin_cam2 Position을 기준으로 cam2의 측정데이터 변환(cam1과 cam2의 theta값 측정을 하기위함)
    pos_ref2_new = _AddCoor(pos_ref2, origin_cam2); //2번 Cam Ref Point
    pos_una2 = _AddCoor(pos_una2, origin_cam2);     //2번 Cam Unalignment Point

    //Line1과 Line2의 Theta측정
    dTheta = Solve2LineAng(pos_ref1, pos_ref2_new, pos_una1, pos_una2);
    ang_final = -dTheta;


    //Estimate Point 계산
    pos_est = FindEstPos(pos_una1, pc, dTheta);
    pos_diff = _SubCoor(pos_ref1, pos_una1);

    //Motor 이동량 데이터계산
    pulse_final[0] = (pos_ref1.y - pos_est.y) * 1 * MM2PULSE;
    pulse_final[1] = (pos_ref1.y - pos_est.y) * (-1) * MM2PULSE;
    pulse_final[2] = (pos_ref1.x - pos_est.x) * 1 * MM2PULSE;

}

bool AlignProcess::isRsltOK(std::vector<CoorData> una_pos, double &diff1, double &diff2)
{
    CoorData pos_una1 = una_pos[0];
    CoorData pos_una2 = una_pos[1];
    double dis1, dis2;

    dis1 = _LenOfCoor(_SubCoor(pos_una1, pos_ref1));
    dis2 = _LenOfCoor(_SubCoor(pos_una2, pos_ref2));
    diff1 = dis1;
    diff2 = dis2;

    if(Tol > (dis1*l) && Tol > (dis2*l))
    {
        return true;
    }
    else
    {
        return false;
    }
}

void AlignProcess::Ang2Pulse(int *ptr, double initAng, double rotAng)
{
    //임의의 각도를 회전시키기 위한, 모터이동데이터(pulse) 계산
    //result[0] = MotorX1, result[1] = MotorX2, result[2] = MotorY

    /*
    int *result = ptr;
    result[0] = round((R * cos((rotAng + initAng + ThetaX1) * PI / 180.0) -
                       R * cos((initAng+ ThetaX1) * PI / 180.0)) * MM2PULSE);
    result[1] = -round(((R * cos((rotAng + initAng+ ThetaX2) * PI / 180.0) -
                         R * cos((initAng+ ThetaX2) * PI / 180.0)) * MM2PULSE));
    result[2] = round((R * sin((rotAng + initAng + ThetaY) * PI / 180.0) -
                       R * sin((initAng + ThetaY) * PI / 180.0)) * MM2PULSE);
    */

}


void AlignProcess::Pulse2MM(double *dst, int *pul)
{
    for(int i=0; i<3; i++)
        dst[i] = pul[i] / MM2PULSE;
}










