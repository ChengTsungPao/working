#include "PLCCom.h"
#include "mainwindow.h"

#include <QtCore>

PLCComProcess::PLCComProcess(){

}

PLCComProcess::~PLCComProcess(){

}

void PLCComProcess::process(){

        while(1){
            if(bStatusPLCPro){
                emit finished();
                break;
            }
            qDebug("PLCComProcess");
            cout << "PLCComProcess" << endl;
            QThread::sleep(10);
        }


}

