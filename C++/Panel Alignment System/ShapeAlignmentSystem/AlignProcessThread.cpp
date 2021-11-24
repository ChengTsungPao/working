#include "AlignProcessThread.h"
#include "mainwindow.h"

#include <QtCore>

AlignProcessThread::AlignProcessThread(QObject *parent, bool b):
    QThread(parent)
{

}

AlignProcessThread::~AlignProcessThread()
{
    this->exit();
}



void AlignProcessThread::run()
{

    while(true)
    {
        sleep(1);

        //Insert code

        //emit ThreadEnd(); //변수,결과데이터,신호 방출 후 프로그램에 알려줌.
        emit have_calculatedval();
    }

}


