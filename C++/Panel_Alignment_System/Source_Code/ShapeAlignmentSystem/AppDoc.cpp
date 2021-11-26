#include "AppDoc.h"
#include "mainwindow.h"

//------------------------------------------------------------------
int nAlignStep = 0;
int nPLCStep = 0;
int nCalStep = 0;

bool bAlignStartReq=false;
bool bAlignComplete=false;
bool bMoving=false;
bool bMovingReq=false;
bool bMovingComplete=false;
bool bAlignResult=false;

//int nAlignCount=0;
int maxAlignCount=5;
double dAlignTol=0.0;



void SetAlignStep(int nStep)
{
    nAlignStep = nStep;
    cout << "Align_SetAlignStep" <<endl;
    cout << nStep << " ";

}

void SetPLCStep(int nStep)
{
    nPLCStep = nStep;
}


void SetCalStep(int nStep)
{
    nCalStep = nStep;
}

QString SetLogSave(QString sMsg)
{
    QString current_time= QDateTime::currentDateTime().toString("[hh:mm:ss:zzz]: ");
    current_time = current_time + sMsg;
    return current_time;

}


int GetAlignStep(void) {return nAlignStep;}
int GetPLCStep(void) {return nPLCStep;}
int GetCalStep(void) {return nCalStep;}
