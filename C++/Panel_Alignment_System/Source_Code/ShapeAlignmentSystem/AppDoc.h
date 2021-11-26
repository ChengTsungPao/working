#ifndef APPDOC_H
#define APPDOC_H

#include <QtCore>
#include <QDate>
#include <QDateTime>
#include "QIODevice"

using namespace std;


extern int nAlignStep;
extern int nPLCStep;
extern int nCalStep;


extern bool bAlignStartReq;
extern bool bAlignComplete;
extern bool bMoving;
extern bool bMovingReq;
extern bool bMovingComplete;
extern bool bAlignResult;
//extern int nAlignCount;
extern int maxAlignCount;
extern double dAlignTol;


typedef struct coordata {
    double x; //x coordinate value
    double y; //y coordinate value
} CoorData;


typedef struct LinePara{
    double a;
    double b;
} LinePara;



void SetAlignStep(int nStep);
void SetPLCStep(int nStep);
void SetCalStep(int nStep);
QString SetLogSave(QString sMsg);

int GetAlignStep(void);
int GetPLCStep(void);
int GetCalStep(void);



#endif // APPDOC_H
