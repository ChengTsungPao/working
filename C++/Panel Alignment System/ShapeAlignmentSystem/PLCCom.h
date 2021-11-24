//PLC와 통신 하는 Thread
#ifndef PLCCOM_H
#define PLCCOM_H


#include <QtCore>

#include "QIODevice"

using namespace std;

//-----------------------------------------------------------------
class PLCComProcess : public QObject
{
    Q_OBJECT

public:
    explicit PLCComProcess();
    ~PLCComProcess();

public:
    bool bStatusPLCPro;

public slots:
    void process(); //여기서 프로세스 내용 진행


signals:
    void finished();
    void error(QString err);

};

#endif // PLCCOM_H
